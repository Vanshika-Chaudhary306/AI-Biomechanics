import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO('yolov8n-pose.pt')

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba = a - b
    bc = c - b
    if np.linalg.norm(ba) == 0 or np.linalg.norm(bc) == 0:
        return 0
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-8)
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return np.degrees(angle)

def process_video(input_path, output_path, sport="Basketball", dominant_side="Right-Side", st_frame=None):
    
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("Error reading video")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    fourcc = cv2.VideoWriter_fourcc(*'VP80')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    frame_count = 0
    last_annotated_frame = None
    current_phase = "Phase 1: Reset/Standing"

    correct_frames = 0
    incorrect_frames = 0
    total_frames = 0
    

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, conf=0.15, verbose=False)
        if results[0].keypoints is None:
            print("No keypoints detected in this frame.")
        annotated_frame = frame.copy()

        try:
            keypoints = results[0].keypoints.xy[0].cpu().numpy()
            if len(keypoints) >= 17:
                if sport == "Basketball":
                            
                            if dominant_side == "Right-Handed":
                                pt1, pt2, pt3 = keypoints[6], keypoints[8], keypoints[10]
                            else:
                                pt1, pt2, pt3 = keypoints[5], keypoints[7], keypoints[9]
                            
                            if pt2[0] != 0 and pt2[1] != 0:
                                angle = int(calculate_angle(pt1, pt2, pt3))
                                wrist_y = pt3[1]
                                shoulder_y = pt1[1]
                                total_frames += 1
                    
                            pt1, pt2, pt3 = keypoints[6], keypoints[8], keypoints[10]
                            
                            if pt2[0] != 0 and pt2[1] != 0:
                                angle = int(calculate_angle(pt1, pt2, pt3))
                                wrist_y = pt3[1]
                                shoulder_y = pt1[1]
                                if wrist_y > shoulder_y:
                                    if current_phase == "Phase 3: Release":
                                        current_phase = "Phase 4: Reset"
                                    elif current_phase != "Phase 4: Reset":
                                        current_phase = "Phase 1: Gather"
                                        
                                elif wrist_y <= shoulder_y:
                                    if angle < 130:
                                        current_phase = "Phase 2: Set Point"
                                    else:
                                        current_phase = "Phase 3: Release"
                                if current_phase == "Phase 1: Gather":
                                    if 70 <= angle <= 110:
                                        text, color = "Good gather pocket", (0, 255, 255)
                                    else:
                                        text, color = "Bring ball to pocket", (0, 0, 255)

                                elif current_phase == "Phase 2: Set Point":
                                    if 85 <= angle <= 110:
                                     correct_frames += 1
                                    else:
                                     incorrect_frames += 1
                                    if 85 <= angle <= 110:
                                        text, color = "Perfect 90-deg Set Point!", (0, 255, 0)
                                    elif angle < 85:
                                        text, color = "Elbow too tight!", (0, 0, 255) 
                                    else:
                                        text, color = "Elbow too wide!", (0, 0, 255)

                                elif current_phase == "Phase 3: Release":
                                    if angle >= 140:
                                     correct_frames += 1
                                    else:
                                     incorrect_frames += 1
                                    if angle >= 140:
                                        text, color = "Excellent Extension!", (0, 255, 0)
                                    else:
                                        text, color = "Extend arm fully!", (0, 0, 255)

                                elif current_phase == "Phase 4: Reset":
                                    text, color = "Shot Complete. Great rep!", (255, 255, 255) 
                                cv2.putText(annotated_frame, current_phase, (int(pt1[0])-40, int(pt1[1])-60), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                                cv2.putText(annotated_frame, f'Angle: {angle}', (int(pt2[0])+10, int(pt2[1])-30), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                                cv2.putText(annotated_frame, text, (int(pt2[0])+10, int(pt2[1])+10), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                                
                                cv2.line(annotated_frame, (int(pt1[0]), int(pt1[1])), (int(pt2[0]), int(pt2[1])), (255, 105, 180), 4) 
                                cv2.line(annotated_frame, (int(pt2[0]), int(pt2[1])), (int(pt3[0]), int(pt3[1])), (255, 105, 180), 4) 

                                for pt in [pt1, pt2, pt3]:
                                    cv2.circle(annotated_frame, (int(pt[0]), int(pt[1])), 8, (0, 255, 0), -1) 
                                    cv2.circle(annotated_frame, (int(pt[0]), int(pt[1])), 12, (0, 255, 0), 2)  
                                cv2.putText(annotated_frame, current_phase, (int(pt1[0])-40, int(pt1[1])-60), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                                cv2.putText(annotated_frame, f'Angle: {angle}', (int(pt2[0])+10, int(pt2[1])-30), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                                cv2.putText(annotated_frame, text, (int(pt2[0])+10, int(pt2[1])+10), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                                
                elif sport == "Football":
                            
                            if dominant_side == "Right-Side":
                                pt1, pt2, pt3 = keypoints[12], keypoints[14], keypoints[16]
                            else:
                                pt1, pt2, pt3 = keypoints[11], keypoints[13], keypoints[15]

                            if pt2[0] != 0 and pt2[1] != 0:
                                angle = int(calculate_angle(pt1, pt2, pt3)) 
                                if current_phase in ["Phase 2: Set Point", "Phase 3: Release"]:
                                    total_frames+=1
                                hip_y = pt1[1]
                                ankle_y = pt3[1]


                                if angle < 120:
                                    current_phase = "Phase 1: Wind-up"
                                    
                                elif 120 <= angle < 160:
                                    if current_phase == "Phase 1: Wind-up" or current_phase == "Phase 2: Strike":
                                        current_phase = "Phase 2: Strike"
                                        
                                elif angle >= 160:
                                    
                                    if ankle_y < (hip_y + 150): 
                                        current_phase = "Phase 3: Follow-through"
                                    else: 
                                        current_phase = "Phase 4: Reset"


                                
                                if current_phase == "Phase 1: Wind-up":
                                    if angle < 100:
                                     correct_frames += 1
                                    else:
                                      incorrect_frames += 1
                                    if angle < 90:
                                        text, color = "Great knee bend! (Max Power)", (0, 255, 0) 
                                    else:
                                        text, color = "Bend knee more for power!", (0, 0, 255) 

                                elif current_phase == "Phase 2: Strike":
                                    text, color = "Locking ankle, extending...", (0, 255, 255) 

                                elif current_phase == "Phase 3: Follow-through":
                                    text, color = "Perfect Extension!", (0, 255, 0) 
                                    if angle >= 160:
                                     correct_frames += 1
                                    else:
                                      incorrect_frames += 1

                                elif current_phase == "Phase 4: Reset":
                                    text, color = "Ready.", (255, 255, 255) 
                                cv2.line(annotated_frame, (int(pt1[0]), int(pt1[1])), (int(pt2[0]), int(pt2[1])), (255, 144, 30), 4) 
                                cv2.line(annotated_frame, (int(pt2[0]), int(pt2[1])), (int(pt3[0]), int(pt3[1])), (255, 144, 30), 4) 
                                for pt in [pt1, pt2, pt3]:
                                    cv2.circle(annotated_frame, (int(pt[0]), int(pt[1])), 8, (0, 255, 255), -1) 
                                    cv2.circle(annotated_frame, (int(pt[0]), int(pt[1])), 12, (0, 255, 255), 2)

                        
                                cv2.putText(annotated_frame, current_phase, (int(pt1[0])-40, int(pt1[1])-60), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                                cv2.putText(annotated_frame, f'Knee Angle: {angle}', (int(pt2[0])+10, int(pt2[1])-30), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                                cv2.putText(annotated_frame, text, (int(pt2[0])+10, int(pt2[1])+10), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                                
        except Exception as e:
            pass

        out.write(annotated_frame)
        if st_frame is not None:
            st_frame.image(annotated_frame, channels="BGR")

        
         
    
    print("Frames:", total_frames)
    print("Correct:", correct_frames)
    print("Incorrect:", incorrect_frames)
    feedback = { "areas": [], "technical": []}
    if total_frames == 0:
     return { "areas": [
            "Poor visibhiility",
            "Incorrect camera angle",
            "Low lighting conditions"
        ],
        "technical": [
            "Pose landmarks could not be detected reliably",
            "Ensure full body is visible in frame",
            "Use a stable side-view recording"
        ]} , 0  

    

    accuracy=(correct_frames / total_frames) * 100
    if accuracy < 50:
        feedback["areas"] = [
            "Elbow alignment",
            "Arm extension",
            "Shot consistency"
        ]

        feedback["technical"] = [
            "Elbow angle frequently deviates from optimal ~90° at set point",
            "Insufficient extension observed during release phase",
            "High variance in motion across frames indicates lack of control"
        ]

    elif accuracy < 75:
        feedback["areas"] = [
            "Release consistency",
            "Elbow positioning",
            "Shot rhythm"
        ]

        feedback["technical"] = [
            "Elbow alignment fluctuates between frames",
            "Release phase lacks smooth transition",
            "Moderate inconsistency in repetition timing"
        ]

    else:
        feedback["areas"] = [
            "Consistency under speed",
            "Balance",
            "Shot rhythm"
        ]

        feedback["technical"] = [
            "Mechanics are correct but vary under motion",
            "Minor instability detected during execution",
            "Timing between phases can be improved"
        ]

    cap.release()
    out.release()
    return feedback, accuracy