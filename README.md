# ewha16-child-abuse-recognition

아동학대 실시간 감지 딥러닝 모델

- Google Colaboratories로 환경구축
- Yolo custom train을 통해 weights 파일 획득
- openpose를 이용해 각가속도 계산
- normalize한 각가속도 데이터를 train 하여 행동인식 모델 생성
- 아동학대 detect 시 aws 서버에 저장되어 웹페이지에 표시


<img src="https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white"/></a>
<img src="https://img.shields.io/badge/OpenCV-3766AB?style=flat-square&logo=OpenCV&logoColor=white&color=red"/></a>
