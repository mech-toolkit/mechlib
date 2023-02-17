# afcai

# Autonomous Fight Club AI - now with YoloV8


1. Create a new python environment (3.10>=Python>=3.7 environment, including PyTorch>=1.7)

2. Make sure this environment is "active"

3. From the cmd prompt run: pip install ultralytics

4. Move the files in the "yolov8" folder into the "ultralytics" folder (this includes the "best_1.pt", "best_2.pt" and most importantly "rfc_server_yolov8.py")

5. Before you start, make sure to upload the latest "rw5.ino" file onto the RoboWarriors you are going to battle. 

6. Once the Robo Warriors are ready, reboot them and place them on the ground.

7. From the cmd prompt, inside the "ultralytics" folder run: python rfc_server_yolov8.py


Note: If you want to use a different model, just add it to the "ultralytics" folder and inside the "rfc_server_yolov8" file, modify the line "model = YOLO('best_2.pt')" with your new model name
```
