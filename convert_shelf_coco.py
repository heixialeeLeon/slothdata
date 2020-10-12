from utils.process_img import LabelmeToCoco

converter = LabelmeToCoco("imgs/shelf_img_cut", "shelf_coco.json")
converter.convert()
