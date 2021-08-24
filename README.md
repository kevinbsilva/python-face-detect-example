### Face Detection Python App

A example of face detection using OpenCV library and imutils. It uses the predefined 
caffe model and deploy.prototxt from OpenCv. 

The application was created following the PyImageSearch tutorial.

The application has two ways of being executed:

1. A video file; 
2. Your own webcam.

To run the app. you can do the following:

For a existing video:

```bash 
python face_detect.py -v path/to/video -p path/to/deploy.prototxt -m path/to/caffe_model
```

If you don't pass the -v argument, it will automatically use the Webcam for face detection.

At the end, it will produce a report containing the timestamp of each detection.