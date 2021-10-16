from imageai.Detection import ObjectDetection
import os

def getTestPeopleCount(path):
	execution_path = os.getcwd()

	detector = ObjectDetection()
	detector.setModelTypeAsRetinaNet()
	detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.1.0.h5"))
	detector.loadModel()
	detections = detector.detectObjectsFromImage(output_type="array", input_image=path)
	# detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , path), output_image_path=os.path.join(execution_path , "shibuya-scranble-new.jpg"))
	# return 0
	
	peopleCount = 0
	for eachObject in detections[1]:
		if eachObject["name"] == "person":
			peopleCount = peopleCount + 1
	return {"people count" : peopleCount}
