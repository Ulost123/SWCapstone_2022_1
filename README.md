# 2022-1 소프트웨어융합캡스톤디자인

## 과제명 : 생성 모델을 이용한 Fisheye image rectification

### 과제 개요 
#### 과제 설계 배경 및 필요성 
- Fisheye lens 는 자율주행자동차, AR, VR 등 시각 지능이 필요한 여러 분야에서 사용된다. 일반 카메라 모델과 다르게 이미지를 생성하는 fisheye lens 의 성질로 인해 해당 이미지를 처리하는 것에 어려움을 겪을 수 있다. 단일 왜곡 계수에 대한 Fisheye image 의 경우 단일한 왜곡 계수를 구하면 되는 문제이지만, 왜곡 계수가 일정 범위 내에서 다양하게 존재할 경우 왜곡 계수를 일일이 구함이 어렵다. 여러 범위의 왜곡 계수, 다른 왜곡 중심점을 기준으로 왜곡된 fisheye image 를 보정하는 데에 딥러닝 모델이 필요할 것 이라고 판단했다.

#### 과제 주요내용
- 이미지 데이터셋을 선정하고, 해당 이미지에 대해 fisheye projection model 을 이용해 fisheye image를 생성한다.
- fisheye image 를 생성할 때 일정 범위 내에서 다양한 왜곡 계수를 가진, 다양한 왜곡 중심점을 가진 fisheye image 들을 생성한다.
- 모델을 통해 보정된 이미지를 생성하고 여러가지 평가지표를 이용해 원본 사진과 얼마나 차이가 있는지 확인한다.
- 생성한 fisheye image 로 훈련한 모델을 이용해 실제 fisheye image 를 보정한다.

#### 최종결과물의 목표
- 일반적인 이미지(perspective image)와 구분하기 힘든 보정된 이미지를 생성하는 것.
- 생성 모델의 이미지 생성 과정에 효과적인 이미지 특징을 추출하는 것
- dynamic fisheye image 에도 robust 한 생성 모델을 만드는 것.
- 실제 fisheye image 의 보정 정도를 확인해보는 것.
- Ground Truth 와 보정된 이미지를 비교했을 때, PSNR >23, SSIM > 0.85

### 과제 수행방법
- Fisheye image rectification 에 관한 자료 조사
- 생성 모델을 이용한 fisheye image rectification 의 선례 논문 조사
- python library(opencv, numpy 등)를 이용한 dynamic fisheye image 생성
- Colab(cloud gpu)을 이용한 모델 학습

### 수행결과
- 본 프로젝트는 “Yang S., Lin C., Liao K., et al.: Progressively complementary network for fisheye image rectification using appearance flow. In: IEEE/CVF conference on computer vision and pattern recognition (2021)” 논문에서 소개된 딥러닝 모델(PCN)과 데이터셋(Places2, 256 * 256 image)을 이용해 진행했다.
- Ground Truth 와 fisheye image 를 training set 각각 40000 장씩, testset 은 각각 10000 장씩 생성해 총 30 epoch 을 학습하는 걸 기준으로 실험들을 진행했다.

#### 실험 1
- 가이드라인으로 잡은 논문과 동일한 범위의 왜곡 계수를 가해 fisheye image 를 생성했고, 이를 이용해 모델을 학습시켰다.

![image](https://user-images.githubusercontent.com/33544078/174228066-98faf36e-9391-4f4a-ba54-743b064e4ba4.png)  ![image](https://user-images.githubusercontent.com/33544078/174228272-93a8a1a1-d989-40d2-bae9-d680e4d6e935.png)


- 위 두 사진 중 좌측이 original image, 우측이 생성한 fisheye image 이다.


![image](https://user-images.githubusercontent.com/33544078/174228498-3bd95980-e749-426d-b40d-7fbb69f050f0.png) 


- 위 세 사진의 좌측부터 차례대로 Fisheye image, Ground truth, 보정된 image 이다. 
- 수치적 평가 결과 PSNR : 23.77 , SSIM : 0.81, MAE : 0.088
- 논문에서 발표한 수치보다 낮은 수치이고, 이는 논문에 비해 학습량이 부족했기에 생긴 결과라고 생각한다.

#### 실험 2
- 이전에 비해 10 배 높인 왜곡 계수의 범위에서 fisheye image 를 생성했고, 이를 이용해 모델을 학습시켰다.


![image](https://user-images.githubusercontent.com/33544078/174228775-317e3e5e-c1f2-4fdf-97a7-f52350b2219d.png)  ![image](https://user-images.githubusercontent.com/33544078/174228911-883ec2b2-288c-4ca9-97c8-1d362d8d6e7a.png)


- 위 두 사진 중 좌측이 original image, 우측이 생성한 fisheye image 이다.


![image](https://user-images.githubusercontent.com/33544078/174228937-6673402d-2c62-44aa-b384-ad560a56a925.png)


- 위 세 사진의 좌측부터 차례대로 Fisheye image, Ground truth, 보정된 image 이다. 
- 수치적 평가 결과 PSNR : 25.63, SSIM : 0.87, MAE : 0.083
- 논문에서 제시한 수치적 평가 수치와 비슷한 수치가 측정되었다.

##### 실험 2로부터 얻은 모델을 이용해, 실험 1의 dataset 보정
- 10 배 높인 왜곡 계수의 범위로부터 생성된 fisheye image 를 학습한 모델을 이용해, 이전 범위(가이드라인 논문과 동일한)의 fisheye image 를 보정했다.


![image](https://user-images.githubusercontent.com/33544078/174230962-9ba24b5f-5324-469c-b69a-faf5a4d4a1e7.png)


- 위 세 사진의 좌측부터 차례대로 Fisheye image, Ground truth, 보정된 image 이다.
- 수치적 평가 결과 PSNR : 17.55, SSIM : 0.52, MAE : 0.19
- 위와 같은 수치가 측정되었고, 이는 아직 모델이 여러 범위의 fisheye image 에 대해 robust 하지 못하다고 판단했다.

#####  실험 1로부터 얻은 모델을 이용해, 실험 2의 dataset 보정
- 반대로 이전 범위(가이드라인 논문과 동일한)의 fisheye image 를 학습한 모델을 이용해, 10 배 높인 왜곡 계
수로부터 생성된 fisheye image 를 보정했다.


![image](https://user-images.githubusercontent.com/33544078/174230906-80bb6474-1e65-46ca-a37c-edfef0cd535e.png)


- 위 세 사진의 좌측부터 차례대로 Fisheye image, Ground truth, 보정된 image 이다.
- 수치적 평가 결과 PSNR : 17.42, SSIM : 0.53, MAE : 0.18
- 이전 실험과 마찬가지로 모델이 여러 범위의 fisheye image 에 대해 robust 하지 못하다고 판단했다.

#### 실험 3
- 두 범위를 모두 포함하는 왜곡 계수의 범위에서 fisheye image 를 생성하여, 모델을 학습시켰다.


![image](https://user-images.githubusercontent.com/33544078/174229107-d28cca76-7184-4837-8d76-012e91dfbd6b.png)  ![image](https://user-images.githubusercontent.com/33544078/174229114-e0cf0397-01a3-4468-9153-22b176ba440f.png)


- 위 두 사진 중 좌측이 original image, 우측이 생성한 fisheye image 이다.


![image](https://user-images.githubusercontent.com/33544078/174229159-a8c12712-ac62-4a67-98e2-eb34a8c41fe9.png)


- 위 세 사진의 좌측부터 차례대로 Fisheye image, Ground truth, 보정된 image 이다. 
- 수치적 평가 결과 PSNR : 24.07, SSIM : 0.82, MAE : 0.094
- 두 범위를 모두 포함하는 왜곡 계수의 범위에서 만든 fisheye image 라서 논문에 비하여 조금 낮은 수치가 측정되었다.
- 이전 실험들에 비해 loss 값이 크고, 픽셀 수준 blur가 뚜렷하게 관찰되었다. 

##### 실험 3의 모델을 이용해 실험1, 2의 dataset보정 
- 이 모델을 활용해 이전 왜곡 계수 범위의 이미지들을 보정하였는데, 강한 왜곡 계수 범위(10 배 높인 범위) 에서는 비슷한 수치 결과가 나왔지만, 원본 범위(10 배 늘리기 전) 에서는 PSNR : 17.73, SSIM : 0.54, MAE : 0.17 의 수치 결과가 측정되었다. 해당 사항에 대한 원인은 아직 파악하지 못했다.

##### 실험 3의 모델 추가 학습
- 이전 실험들에 비해 loss 값이 크고, 보정된 이미지의 픽셀 수준에서 blur 가 보이는 관계로 20 epoch추가 학습을 시켰다. 


![image](https://user-images.githubusercontent.com/33544078/174230032-8287b282-1761-44ed-a783-b43a544a4a41.png)


- 좌측이 추가 학습 이전의 보정결과, 우측이 추가 학습 이후의 보정결과이다. 
- 추가 학습 이전과 비슷한 수치적 결과를 얻을 수 있었다.

#### 실험 4
- 왜곡 중심점을 이미지 정중앙에서 이미지 중앙의 8 * 8 정사각형 모양의 픽셀들 중 하나로 변화시키고, 왜곡 계수의 범위는 논문 원본 그대로를 이용해 실험을 진행했다.


![image](https://user-images.githubusercontent.com/33544078/174229944-d27c1aa0-4055-40f6-9b0c-7b50dc0bc2e7.png)


- 좌측은 중심점이 이미지 정가운데, 우측은 중심점을 조금 변경시킨 이미지이다.


![image](https://user-images.githubusercontent.com/33544078/174230091-9b97c58d-0383-4055-abad-862592f32c9c.png)


- 위 세 사진의 좌측부터 차례대로 Fisheye image, Ground truth, 보정된 image 이다. 
- PSNR : 23.9, SSIM : 0.804, MAE : 0.097
- 다음과 같은 수치결과를 얻었으며, 이전 실험들과 비슷한 수치 값을 측정할 수 있었다.
- 중심점의 변화를 크게 주지 않았기 때문에 비슷한 수치 값을 측정할 수 있었다고 생각한다.

#### 실험 3의 모델을 이용한 실제 fisheye image 보정
- 가장 많이 학습을 시킨 모델(50 epoch)을 이용해 지도 교수님으로부터 받은 실제 fisheye image(fisheye lens로 얻은 image)와 Woodscape dataset (실제 fisheye image dataset)을 보정하는 실험을 진행했다.


![image](https://user-images.githubusercontent.com/33544078/174230566-2d51ddda-4ef9-4f85-99b0-0025c1fce154.png)


- 좌측이 실제 fisheye image(모델에 넣을 수 있도록 수정한 image), 우측이 보정된 image 이다.
- 실제 fisheye image 에 대한 Ground Truth 가 존재하지 않기 때문에 수치적 평가는 진행하지 못했다.
- 보정이 되는 모습을 보였으나, 애초에 실제 fisheye image 가 큰 해상도를 갖고 있고 모델은 256 크기의 이 미지를 기반으로 학습되어 있어 보정된 image 가 좋지 않은 화질을 가지게 되었다.
- 실제 fisheye image 를 보정하기 위해서는 resolution 관련 해결방안이 필요하다고 생각했다.

### 결론 및 아쉬운 점
- 가이드라인 논문에 소개된 모델을 이용해 다양한 왜곡 계수 범위, 중앙이 아닌 다른 왜곡 중심점을 갖는
fisheye image 를 생성하고 이를 학습 및 평가했다
- 논문에서보다 더 넓은 범위의 fisheye image 를 학습해서 평가해봤고, 이전 좁은 범위보다 수치적 결과는 낮
게 측정되었지만 모델의 구조 혹은 다른 하이퍼 파라미터들을 수정하면 더 넓은 범위에서도 논문에서만큼
의 수치적 결과를 얻을 수 있을 것으로 예상된다.
- 진행한 프로젝트의 한계점은 모델의 구조에 대해 수정, 개선했던 점이 없고 보정된 fisheye image 를 다른
task(Object detection 과 같은 vision algorithm)에 적용해보지 못했다는 것이다. 또한 실제 fisheye image
보정에 있어서 resolution 문제를 해결해야 양질의 보정이 가능하다는 것을 깨달았다.
- 향후 계획은 모델 구조를 수정, 개선하고 실제 fishseye image 를 잘 보정할 수 있는 방향으로 계속 진행해 나갈 예정이다.

### 참고자료
#### 논문
- Yang S., Lin C., Liao K., et al.: Progressively complementary network for fisheye image rectification using appearance flow. In: IEEE/CVF conference on computer vision and pattern recognition (2021)
- Xue, Zhu-Cun, Nan Xue, and Gui-Song Xia. "Fisheye distortion rectification from deep straight lines." arXiv preprint arXiv:2003.11386 (2020).
- Yin, Xiaoqing, et al. "Fisheyerecnet: A multi-context collaborative deep network for fisheye image rectification." Proceedings of the European conference on computer vision (ECCV). 2018.
#### dataset
- http://places2.csail.mit.edu/download.html - places2 dataset(places365-standard small images)
#### 그 외 참고 홈페이지
- https://github.com/uof1745-cmd/PCN - 가이드라인 논문 구현 공식 github
- https://en.wikipedia.org/wiki/Fisheye_lens – 위키피디아, ‘fisheye lens’
- https://www.cv-learn.com/20210222-image-projection/ - ‘image projection 이란?’ (블로그)
- https://darkpgmr.tistory.com/31 - ‘다크프로그래머 :: 카메라 왜곡보정 – 이론 및 실제’(블로그)
- https://darkpgmr.tistory.com/32 - ‘다크프로그래머 :: 카메라 캘리브레이션’(블로그)


