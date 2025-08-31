---
title: "어릴 적 사진으로 미래 모습 만들기"
date: 2025-08-31 14:30:00 +0900
categories: [AI]
tags: [토이프로젝트, 바이브코딩, 웹앱]
---

## Google 나노 바나나로 어릴 적 사진으로 미래 모습 만들기

> 어릴 적 사진 한 장으로 당신의 미래를 그려보세요.

누구나 한 번쯤 '내가 나이가 들면 어떤 모습일까?' 궁금해한 적이 있을 겁니다. 최근 공개된 Google의 나노 바나나 API를 사용하여, 어릴 적 사진 한 장만으로 10대부터 70대까지의 미래 모습을 생성해주는 토이 프로젝트, **'인생 파노라마 스튜디오'**를 만들어 보았습니다.


### ✨ 주요 기능

이 웹 애플리케이션의 기능은 매우 간단하고 직관적입니다.

* **사진 업로드**: 미래 여행의 시작점이 될 어린 시절 사진(JPG, PNG)을 업로드합니다.
* **API 키 입력**: Google AI Studio에서 발급받은 Gemini API 키를 입력하여 AI 모델을 활성화합니다.
* **미래 모습 생성**: 버튼 클릭 한 번으로 AI가 10대, 20대, 30대, 40대, 50대, 70대의 모습을 순차적으로 생성합니다.
* **결과 확인 및 다운로드**: 생성된 각 시대별 사진을 클릭하여 크게 보거나, 개별적으로 저장할 수 있습니다. '모두 저장하기' 기능으로 모든 결과물을 ZIP 파일 하나로 받을 수도 있습니다.

### 💻 기술 스택 및 작동 원리

이 프로젝트는 별도의 백엔드 서버 없이 프론트엔드 기술만으로 구현되었습니다.

* **언어**: `HTML`, `CSS`, `JavaScript` (Vanilla JS)
* **스타일링**: `TailwindCSS`
* **핵심 API**: `Google Gemini API (gemini-2.5-flash-image-preview)`
* **라이브러리**: `JSZip` (이미지 전체 다운로드 기능)

가장 핵심적인 부분은 사용자가 업로드한 이미지와 각 세대별 프롬프트를 Gemini API에 전송하여 새로운 이미지를 생성하는 로직입니다. `gemini-2.5-flash-image-preview` 모델은 텍스트와 이미지를 동시에 입력받아 이미지를 출력하는 멀티모달(Multi-modal) 기능을 가지고 있어 이런 작업에 매우 적합합니다.

구현은 JavaScript의 `fetch` 함수를 사용하여 비동기적으로 API를 호출하는 방식으로 이루어집니다. 사용자가 '생성하기' 버튼을 누르면, 업로드된 원본 이미지는 Base64 형식으로 인코딩됩니다. 이 이미지 데이터는 각 세대에 맞는 텍스트 프롬프트와 함께 JSON 객체로 구성되어 Gemini API 엔드포인트로 전송됩니다. API로부터 이미지 데이터가 포함된 응답을 받으면, 이를 파싱하여 화면의 각 세대별 카드에 표시해 줍니다.

### 📝 세대별 이미지 생성을 위한 프롬프트

결과물의 품질을 결정하는 가장 중요한 요소는 바로 **프롬프트**입니다. 원본 이미지의 핵심적인 특징(인종, 성별, 얼굴 구조)은 유지하면서 나이만 자연스럽게 변화시키기 위해, 각 세대별로 다음과 같이 구체적인 프롬프트를 사용했습니다.

* **10대**: `"A highly realistic photograph of the person from the original image, aged up to be in their late teens (around 18 years old). Their core facial features, ethnicity, and gender must be preserved. A high school graduation or early university style portrait with a bright, hopeful expression. The photo should look like it was taken with a modern digital camera. The image must not contain any text or letters."`
* **20대**: `"A highly realistic photograph of the person from the original image, aged up to be in their mid-20s. Their core facial features, ethnicity, and gender must be preserved. A candid photo of a young professional or traveler, looking confident in contemporary fashion... "`
* **30대**: `"A highly realistic photograph of the person from the original image, aged up to be in their mid-30s. Their core facial features, ethnicity, and gender must be preserved. A professional or warm family environmental portrait, showing confidence and maturity... "`
* **40대**: `"A highly realistic, relaxed photograph of the person from the original image, aged up to be in their mid-40s. Their core facial features, ethnicity, and gender must be preserved. They are enjoying a hobby or a casual social gathering, looking comfortable and content... "`
* **50대**: `"A highly realistic, dignified portrait of the person from the original image, aged up to be in their mid-50s. Their core facial features, ethnicity, and gender must be preserved. They look accomplished and wise. The setting is a nice home or office... "`
* **70대**: `"A highly realistic, warm, and heartwarming photograph of the person from the original image, aged up to be in their 70s. Their core facial features, ethnicity, and gender must be preserved. They have laugh lines and a gentle, happy expression... "`

**나노 바나나 프롬프트 참고**: [https://tigerjk9.github.io/ai/nano-banana/](https://tigerjk9.github.io/ai/nano-banana/)

![원본 사진과 변환된 사진 비교](/assets/lifepanorama.png)

### 🚀 마치며

'인생 파노라마 스튜디오'는 Gemini와 같은 강력한 AI 모델을 활용하면 복잡한 서버 없이도 얼마나 창의적이고 재미있는 웹 애플리케이션을 만들 수 있는지 보여주는 좋은 예시라고 생각합니다. 프롬프트 엔지니어링을 통해 결과물을 세밀하게 제어하는 과정도 매우 흥미로웠습니다.

여러분도 이 프로젝트를 참고하여 자신만의 아이디어를 실현해 보시는 건 어떨까요?

* 🌐 **라이브 데모**: [https://life-panorama.netlify.app/](https://life-panorama.netlify.app/)
* 🌐 **유사 토이 프로젝트**: [nostalgia-photo-studio.netlify.app](https://nostalgia-photo-studio.netlify.app)
* 🔗 **GitHub 저장소**: [https://github.com/tigerjk9/life-panorama-studio](https://github.com/tigerjk9/life-panorama-studio)
