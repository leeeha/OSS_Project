# 추억의 오락실 Pang 게임  

## 게임 조건 

- 큰 공 1개가 나타나서 스크린 내에서 움직인다. 
- 캐릭터는 스테이지 바로 위에 위치하며, 좌우로만 이동 가능하다. 
- 스페이스 바를 누르면 무기를 쏘아 올릴 수 있다. 
- 무기로 공을 맞히면 공이 절반 크기로 쪼개지며, 가장 작은 크기의 공은 없어진다.
- 무기로 공을 맞힐 때마다 점수가 증가한다. (작은 공일수록 큰 점수)
- 다음과 같은 조건에서 게임이 종료된다.
    - 모든 공을 없앤 경우, Mission Completed (성공)
    - 캐릭터가 공에 맞으면, Game Over (실패)
    - 시간 제한 100초를 초과하면, Time Over (실패)
- FPS는 30으로 고정한다. (필요 시 speed 값을 조정)

- 무기로 공을 맞힐 때마다 점수 증가 (10, 30, 50, 100)
- 100점을 넘기면 아이템 등장 
- 난이도에 따라 공의 이동 속도를 빠르게 해보자.
- 사운드도 추가할 수 있겠다. 충돌하거나 아이템 먹었을 때 

## 알고리즘 

1. 파이게임 초기화 
2. 게임에 사용되는 요소들 초기화 (배경 화면, 이미지, 좌표, 속도, 폰트 등)
3. 키 입력에 따라 위치 변화량 조절
4. 요소들의 위치 정의
5. 요소들 간의 충돌 처리 
6. 화면에 그리기

## 게임 이미지 크기 

- 스크린: 800 * 500 
- 배경: 800 * 450 - background.png
- 스테이지: 800 * 30 - stage.png
- 스코어보드: 800 * 50 - scoreboard.png
- 캐릭터: 30 * 60 - character.png
- 무기: 20 * 400 - weapon.png
- 공: 160 * 160, 80 * 80, 40 * 40, 20 * 20 - balloon1.png ~ balloon4.png

## 참고자료 

https://youtu.be/Dkx8Pl6QKW0 

## 라이센스 

[MIT License](https://github.com/leeeha/OSS_Project/blob/main/license)