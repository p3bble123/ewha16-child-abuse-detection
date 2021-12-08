
![header](https://capsule-render.vercel.app/api?type=waving&color=gradient&height=280&text=그로쓰%2016팀%20아이를지켜조&desc=KIDOW&fontColor=ffffff&fontSize=50&fontAlign=50&fontAlignY=40&descSize=25&descAlign=50&descAlignY=55)  

# AI 아동학대 실시간 감지 시스템 KIDOW <image src="https://user-images.githubusercontent.com/71063574/145254163-8c8e5b1c-1c03-4052-b4b5-870ca97ebe93.png"  width="40" height="40">

:link: **관련링크** <a href="https://m.youtube.com/watch?v=l2cwnvP0w5s"><img src="https://img.shields.io/badge/Youtube-3766AB?style=flat-square&logo=YouTube&logoColor=white&color=red&link=내링크"/></a> <a href="https://drive.google.com/file/d/1fzgPNdyGTnzvcMkRXTbUQq1-1Dv0BtUc/view?usp=sharing"><img src="https://img.shields.io/badge/Poster-3766AB?style=flat-square&color=blue&link=내링크"/></a>  

:heart: **기술블로그** <a href="https://creamlove08.tistory.com/"><img src="https://img.shields.io/badge/HeejinKim-3766AB?style=flat-square&color=D3E4CD&link=내링크"/></a> <a href="https://creamlove08.tistory.com/"><img src="https://img.shields.io/badge/MinheeJo-3766AB?style=flat-square&color=99A799&link=내링크"/></a> <a href="https://creamlove08.tistory.com/"><img src="https://img.shields.io/badge/JihyeonMa-3766AB?style=flat-square&color=F2DDC1&link=내링크"/></a>
  
  
  
## 구현 방법

신체적인 공격 행위를 어떻게 인식할 것인가? 또한 이를 유사 행위(쓰다듬기 등)와 어떻게 구분할 것인가에 대한 부분이 이 알고리즘의 핵심이다. 간단한 상황을 예로 들자. 보육교사가 아이의 머리를 쓰다듬는 장면(유사행위)과 아이의 머리를 가격하는 장면(폭력 행위)에서 전자의 장면에서 보육교사는 팔에 과도한 힘을 가하지 않기 때문에 움직이는 팔에 해당하는 벡터의 크기는 크게 나타나지 않을 것이다. 또한 이 결과로 아이의 머리 keypoint는 크게 움직이지 않는다. 하지만 후자의 장면에서는 팔에 강한 힘을 주기 때문에 움직이는 팔에서 계산된 벡터의 크기는 큰 값을 가지게 될 것이고 이 결과 아이의 머리Key point 는 크게 움직일 것이다. 따라서 우리는 폭력 인식을 위하여 입력 인터페이스로 받은 영상 시퀀스에서 접촉 여부, 벡터의 크기, keypoint의 방향 벡터를 구하여 폭력 인식을 추론한다. 

  yolo는 기존의 다른 이미지 분석 모델과 달리 한장의 이미지를 한번만 분석하여 결과를 도출하기 때문에 속도와 성능면에서 실시간 검출에 탁월하다. 따라서 실시간 검출에 적합한 모델이기에 폭력 검출 알고리즘에 적용하였다. 학습시킨 YOLO를 통해 접촉 여부가 인식된다면 해당 영상 시퀀스는 라벨링 작업을 거쳐 클래스로 검출된다. 이후 클래스로 라벨링된 영상 시퀀스는 OpenPose를 통하여 관절을 포함한 사람의 18개의 keypoint가 검출된다. 검출된 keypoint에서 방향 벡터가 계산되고 해당 벡터가 LSTM의 입력값이 된다. 또한 가속도를 검출하기 위해서 Optical flow를 계산한다. Optical flow란 연속하는 두 프레임에서 카메라 또는 객체의 움직임에 의해 나타나는 객체의 이동 정보 패턴을 말하며 밀집 옵티컬 플로우 함수를 사용하여 프레임 내의 옵티컬 플로우를 출력값으로 받아 사용한다. 받은 출력값을 극좌표계로 변경하여 벡터의 크기를 얻고 LSTM의 입력값이 된다. 영상 시퀀스의 벡터의 크기와 keypoint의 방향벡터를 입력값으로 받는 LSTM은 이를 Sequence로 학습하게 된다.  
  
  LSTM은 입력(input), 망각(forget),출력(output) 세 개의 게이트를 통해 입출력과 기억을 조절해 영상 시퀀스의 문맥을 학습하게 된다. 아이의 머리를 때리기 직전까지의 영상 시퀀스의 프레임들은 어른의 팔에서 큰 벡터의 크기와 방향을 가지게 된다. 그리고 이후의 영상 시퀀스의 프레임들은 아이의 머리에서 벡터의 크기와 방향을 가지게 된다. 이 문맥이 LSTM에 학습되고 최종적으로 폭력으로 검출한다.
  
  정신적 학대는 맥박 데이터를 가져와 이상치 맥박과 산소포화도를 통한 스트레스 지수를 검출한다. 두 결과값 모두 정상 범위를 넘어서면 동영상이 저장되어 파일이 홈페이지에 올라간다.  
  
  
  
  
  
  

## Tech
<img src="https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white"/></a>
<img src="https://img.shields.io/badge/OpenCV-3766AB?style=flat-square&logo=OpenCV&logoColor=49FF00&color=red"/></a>
<img src="https://img.shields.io/badge/YOLO-3766AB?style=flat-square&color=84DFFF"/></a>
<img src="https://img.shields.io/badge/OpenPose-3766AB?style=flat-square&color=grey"/></a>
<img src="https://img.shields.io/badge/TensorFlow-3766AB?style=flat-square&logo=TensorFlow&logoColor=yellow&color=orange"/></a>
<img src="https://img.shields.io/badge/React.js-3766AB?style=flat-square&logo=React&logoColor=black&color=84DFFF"/></a>
<img src="https://img.shields.io/badge/AWS-3766AB?style=flat-square&logo=Amazon AWS&logoColor=orange&color=E8E1D9"/></a>

KIDOW uses a number of open source projects to work properly:

- Python - version.3 환경
- [OpenCV] - 다양한 영상 및 동영상 데이터 처리
- [YOLO] - 빠른 처리속도로 실시간으로 객체탐지가 가능함
- [OpenPose] - 실시간으로 여러사람의 자세를 추정할 수 있는 API
- [Tensorflow] - 순환신경망 모델 구축
- [React.js] - 웹앱 구축을 위한 JavaScript 라이브러리
- [AWS] - 클라우드 플랫폼
- [Colab] - 딥러닝 코드를 실행하기 위한 가상서버

And of course KIDOW itself is open source with a [public repository][dill]
on GitHub.  




## 기대효과 및 의의
  제안하는 아동폭력 실시간 감지 시스템은 “어린이집 정보공개 포털사이트 (https://info.childcare.go.kr/info/main.jsp)” 내에 어린이집 평가등급과 인증점수가 낮은 어린이집을 우선적으로 선정하여 적용될 것이며, 위탁가정이나 폭력 신고 접수 내역이 있는 가정환경으로 그 사용성을 확장시킬 수 있을 것이다. 제안하는 시스템이 보육시설이 아닌 가정환경에 적용될 경우 가정 내의 사생활 침해가 발생할 우려가 있으므로, 화재방지센서처럼 아동학대 정황만을 감지할 수 있도록 한다. 그후 데이터를 관리하고 학대 상황 발생 시 재빠르게 상황에 대처할 수 있도록 하는 정부차원의 노력이 필요할 것이다.
  
  이 시스템은 어른과 미취학 아동 사이에서 발생한 폭력뿐만 아니라 폭력이 발생할 가능성이 있는 모든 환경에 적용시킬 수 있다. 일례로, 길거리에서 묻지마 폭행 사건이 발생했을 경우, 가해자를 추려내는데 폭력감지 내역 로그 정보를 활용하는 것이 수사에 큰 도움이 될 것이다. 유치원 보육시설을 넘어 실시간 폭력감지 시스템 기능을 확장시켜 다양한 곳에 응용/적용 시킬 수 있을 것이다.  
 
  아동학대 방지는 무엇보다 조기 탐지가 중요하다. 제안하는 서비스의 기대효과는 인공지능으로 아동학대를 실시간으로 탐지하여 초기대응이 가능하다는 것이다. 기존의 아동학대 방지 시스템들은 모두 1차적이고 예방적인 접근을 목적으로 하기에 아동학대의 조기탐지 혹은 실시간탐지 기능은 떨어질 수밖에 없다. 하지만 인공지능 모델을 도입한 제안 시스템은 이상탐지를 위한 특징들을 추출하고 학습하여 아동학대를 실시간으로 탐지할 수 있는 좋은 수단이 된다. 또한 이 시스템을 통해 아동학대 피해 가정이 개인정보 보호법 CCTV영상을 확보하는데 어려움을 겪는 것을 해소해 줄 수 있으며, 결과적으로 전반적인 우리사회의 건강한 양육 환경 조성하는데 기여할 수 있다.  
  
  
  
  

## References
* YOLO custom: <https://github.com/theAIGuysCode/YOLOv4-Cloud-Tutorial>
* OpenPose demo: <https://github.com/tugstugi/dl-colab-notebooks>
* keras model: <https://keras.io/ko/getting-started/sequential-model-guide/>  




## License

MIT



[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [dill]: <https://github.com/p3bble123/ewha16-child-abuse-detection>
   [OpenCV]: <https://opencv.org/>
   [YOLO]: <https://pjreddie.com/darknet/yolo/>
   [OpenPose]: <https://github.com/CMU-Perceptual-Computing-Lab/openpose>
   [Tensorflow]: <https://www.tensorflow.org/?hl=ko>
   [React.js]: <https://ko.reactjs.org/>
   [AWS]: <https://aws.amazon.com/ko/free/?trk=fa2d6ba3-df80-4d24-a453-bf30ad163af9&sc_channel=ps&sc_campaign=acquisition&sc_medium=ACQ-P|PS-GO|Brand|Desktop|SU|Core-Main|Core|KR|KR|Text&ef_id=Cj0KCQiAzMGNBhCyARIsANpUkzPOCj0N5URZsuoJpkQeONcmxqitPMfjwJa7pBsP5PcRENpe9PNElPYaAp9nEALw_wcB:G:s&s_kwcid=AL!4422!3!563761819834!e!!g!!aws&ef_id=Cj0KCQiAzMGNBhCyARIsANpUkzPOCj0N5URZsuoJpkQeONcmxqitPMfjwJa7pBsP5PcRENpe9PNElPYaAp9nEALw_wcB:G:s&s_kwcid=AL!4422!3!563761819834!e!!g!!aws&all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=*all>
   [Colab]: <https://colab.research.google.com/?utm_source=scs-index>
