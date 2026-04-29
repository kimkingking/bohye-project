# 다이어트 식단 기록 앱 (K8s / Kasten 테스트용)

이 프로젝트는 쿠버네티스 환경에서 MySQL과 함께 배포되도록 설계된 간단한 식단 기록 애플리케이션입니다.
백업 솔루션(Kasten) 등을 통한 데이터 복구 테스트를 목적으로 합니다.

## 1. 주요 기능
- 식단 기록 추가 (날짜, 음식, 칼로리, 메모)
- 데이터베이스(MySQL) 기반 목록 자동 최신화
- 컨테이너 시작 시 DB 테이블 자동 초기화 (Init Logic 포함)

## 2. 환경 변수 설정
애플리케이션은 다음 환경 변수를 통해 MySQL에 접속합니다:
- `DB_HOST`: MySQL 서버 호스트 (기본값: `localhost`)
- `DB_USER`: 접속 사용자명 (기본값: `root`)
- `DB_PASSWORD`: 접속 비밀번호 (기본값: `password`)
- `DB_NAME`: 사용할 데이터베이스명 (기본값: `diet_db`)

## 3. 로컬 빌드 및 실행 (Docker)
```bash
# 이미지 빌드
docker build -t diet-log-app .

# 컨테이너 실행 (MySQL이 이미 실행 중이라고 가정)
docker run -d -p 3000:3000 \
  -e DB_HOST=172.17.0.1 \
  -e DB_USER=root \
  -e DB_PASSWORD=your_password \
  diet-log-app
```

## 4. Kubernetes 배포 팁
쿠버네티스에서 실행할 때는 `Deployment`와 `Service`를 정의하고, MySQL은 `StatefulSet`이나 외부 RDS를 사용할 수 있습니다.
- 백업 테스트 시, 데이터를 입력한 후 Kasten을 사용하여 MySQL의 Persistent Volume(PV)을 스냅샷하고 복구하여 데이터 정합성을 확인하세요.
