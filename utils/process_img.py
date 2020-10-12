import os
import os.path as osp
import glob
import json
import cv2
import numpy as np

def cut_img_and_json(img_path, save_root, mode="tb", json_only=False):
    assert mode in ["tb", "tblr"]
    json_path = img_path[:-4] + ".json"
    if not osp.exists(json_path):
        print("json {} not exists.".format(json_path))

    img_name = osp.split(img_path)[-1]
    stem, ext = osp.splitext(img_name)
    img = cv2.imread(img_path)
    h, w = img.shape[:2]
    json_data = json.load(open(json_path, "r"))

    if mode == "tb":
        if not json_only:
            img_t = img[:h//2, :]
            img_b = img[h//2:, :]
            
            cv2.imwrite(osp.join(save_root, f"{stem}_t{ext}"), img_t)
            cv2.imwrite(osp.join(save_root, f"{stem}_b{ext}"), img_b)

        json_t = {
            "version": "",
            "flags": {},
            "shapes": [],
            "imagePath": f"{stem}_t{ext}",
            "imageData": None,
            "imageHeight": h // 2,
            "imageWidth": w
        }
        json_b = {
            "version": "",
            "flags": {},
            "shapes": [],
            "imagePath": f"{stem}_b{ext}",
            "imageData": None,
            "imageHeight": h - h // 2,
            "imageWidth": w
        }

        for item in json_data["shapes"]:
            pts = np.array(item["points"])
            c = pts.mean(0)
            if c[1] < h // 2:
                json_t["shapes"].append(item)
            elif c[1] >= h // 2:
                pts[:, 1] -= h // 2
                item["points"] = pts.tolist()
                json_b["shapes"].append(item)

        with open(osp.join(save_root, f"{stem}_t.json"), "w") as f:
            json.dump(json_t, f)
        with open(osp.join(save_root, f"{stem}_b.json"), "w") as f:
            json.dump(json_b, f)

    elif mode == "tblr":
        if not json_only:
            img_tl = img[:h//2, :w//2]
            img_tr = img[:h//2, w//2:]
            img_bl = img[h//2:, :w//2]
            img_br = img[h//2:, w//2:]

            cv2.imwrite(osp.join(osp.join(save_root, f"{stem}_tl{ext}")), img_tl)
            cv2.imwrite(osp.join(osp.join(save_root, f"{stem}_tr{ext}")), img_tr)
            cv2.imwrite(osp.join(osp.join(save_root, f"{stem}_bl{ext}")), img_bl)
            cv2.imwrite(osp.join(osp.join(save_root, f"{stem}_br{ext}")), img_br)

        json_tl = {
            "version": "",
            "flags": {},
            "shapes": [],
            "imagePath": f"{stem}_tl{ext}",
            "imageData": None,
            "imageHeight": h // 2,
            "imageWidth": w // 2
        }
        json_tr = {
            "version": "",
            "flags": {},
            "shapes": [],
            "imagePath": f"{stem}_tr{ext}",
            "imageData": None,
            "imageHeight": h // 2,
            "imageWidth": w - w // 2
        }
        json_bl = {
            "version": "",
            "flags": {},
            "shapes": [],
            "imagePath": f"{stem}_bl{ext}",
            "imageData": None,
            "imageHeight": h - h // 2,
            "imageWidth": w // 2
        }
        json_br = {
            "version": "",
            "flags": {},
            "shapes": [],
            "imagePath": f"{stem}_br{ext}",
            "imageData": None,
            "imageHeight": h - h // 2,
            "imageWidth": w - w // 2
        }

        for item in json_data["shapes"]:
            pts = np.array(item["points"])
            c = pts.mean(0)
            if c[1] < h // 2 and c[0] < w // 2:
                json_tl["shapes"].append(item)
            elif c[1] < h // 2 and c[0] >= w // 2:
                pts[:, 0] -= w // 2
                item["points"] = pts.tolist()
                json_tr["shapes"].append(item)
            elif c[1] >= h // 2 and c[0] < w // 2:
                pts[:, 1] -= h // 2
                item["points"] = pts.tolist()
                json_bl["shapes"].append(item)
            elif c[1] >= h // 2 and c[0] >= w // 2:
                pts[:, 0] -= w // 2
                pts[:, 1] -= h // 2
                item["points"] = pts.tolist()
                json_br["shapes"].append(item)

        with open(osp.join(save_root, f"{stem}_tl.json"), "w") as f:
            json.dump(json_tl, f)
        with open(osp.join(save_root, f"{stem}_tr.json"), "w") as f:
            json.dump(json_tr, f)
        with open(osp.join(save_root, f"{stem}_bl.json"), "w") as f:
            json.dump(json_bl, f)
        with open(osp.join(save_root, f"{stem}_br.json"), "w") as f:
            json.dump(json_br, f)


class LabelmeToCoco(object):
    def __init__(self, json_root, save_path):
        super().__init__()
        self.json_root = json_root
        self.save_path = save_path

    def convert(self):
        coco_data = {"images": [], "categories": [], "annotations": []}
        coco_data["categories"] = [{"supercategory": "object", "id": 1, "name": "object"}] # Only use single category
        ann_id = 0
        for img_id, json_path in enumerate(glob.glob(osp.join(self.json_root, "*.json"))):
            sample = json.load(open(json_path))
            coco_data["images"].append({
                "id": img_id, "file_name": sample["imagePath"], "height": sample["imageHeight"], "width": sample["imageWidth"]
            })
            for shape in sample["shapes"]:
                if shape["label"] == "1056817": # Now we don't care the whole space in the freezer
                    continue
                pts = np.array(shape["points"])
                pts_min = np.amin(pts, axis=0)
                pts_max = np.amax(pts, axis=0)
                wh = pts_max - pts_min
                        
                annotation = {
                    'segmentation': pts.flatten().tolist(),
                    'iscrowd': 0,
                    'image_id': img_id,
                    'bbox': [pts_min[0], pts_min[1], wh[0], wh[1]],
                    'area': wh[0] * wh[1],
                    'category_id': 1,
                    'id': ann_id
                }
                ann_id += 1
                coco_data["annotations"].append(annotation)

        class MyEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, np.ndarray):
                    return obj.tolist()
                else:
                    return super(MyEncoder, self).default(obj)
        with open(self.save_path, "w") as f:
            json.dump(coco_data, f, cls=MyEncoder)
