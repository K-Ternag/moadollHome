# MoaDoll · 모아돌 홈페이지

GitHub Pages용 한국어·영어 정적 홈페이지입니다. `D:\Projects\foutFoldHome`의 다국어·정책·지원 페이지 구성을 참고하고, 모아돌의 실제 기능과 제공된 이미지에 맞춰 새로 제작했습니다.

- 한국어: [index.html](index.html)
- 영어: [index.en.html](index.en.html)
- 사이트 폴더: `D:\Projects\characterGameHome`
- 앱 소스 확인 기준: `com.moadoll`, `0.12.2-current-card-share`, versionCode 40
- 저장소: https://github.com/K-Ternag/moadollHome
- GitHub Pages 주소: https://k-ternag.github.io/moadollHome/ (실제 공개 여부는 저장소 Pages 설정과 배포 결과에서 확인)

## 바로 보기

`index.html`을 브라우저에서 열 수 있습니다. 로컬 HTTP로 확인하려면 이 폴더에서 실행하세요.

```powershell
python -m http.server 8080 --bind 127.0.0.1
```

`http://127.0.0.1:8080/`으로 접속합니다. 사이트 실행에는 설치나 빌드가 필요하지 않습니다. 외부 폰트·분석 도구·쿠키·CDN 라이브러리를 사용하지 않습니다.

## 페이지

각 페이지는 `.en.html` 영어 버전도 제공합니다. 언어 전환은 같은 페이지와 앵커를 유지합니다.

| 경로 | 내용 |
| --- | --- |
| `index.html` | 게임 소개, 4개 기능 미리보기, 이미지 확대, 이용 흐름, 출시 안내 |
| `guide.html` | 인형 꾸미기, 헤어 색상, 포토카드, PNG 저장·공유 안내 |
| `support.html` | FAQ, 연락처 및 메일 문의 |
| `privacy.html` | 개인정보처리방침 |
| `delete-account.html` | 기기 데이터·갤러리·백업·문의 기록 삭제 안내 |
| `terms.html` | 이용약관 |
| `404.html` | 없는 주소 안내 |

정책 본문·운영 정보·문의 링크는 HTML에 직접 생성됩니다. JavaScript를 꺼도 읽을 수 있으며 기본 메뉴·FAQ·이미지 원본 링크도 사용할 수 있습니다. JavaScript는 모바일 메뉴, 접근 가능한 탭, 이미지 확대, 언어 간 앵커 유지에만 사용합니다.

## 이미지

| 언어 | 사용한 원본 | 사이트 내 위치 |
| --- | --- | --- |
| 한국어 | `D:\Projects\characterGame\output\store-marketing-v3\website\*.jpg` | `assets/ko/` |
| 영어 | `D:\Projects\characterGame\output\website-en\website\*-en.jpg` | `assets/en/` |

각 언어의 4개 JPG를 원본 그대로 복사했습니다. 영어 원본의 파일명에서만 `-en`을 제거했습니다. PNG보다 작은 JPG를 사용하며, 8개 이미지 전체가 약 2.3 MB입니다. 영어 홍보 이미지에 남아 있는 한국어 앱 UI·카드 문구는 원본 그대로 유지합니다. 영문 페이지에도 이 점을 안내합니다. 첫 화면의 카드는 원본 이미지의 일부를 CSS로 표시하며 원본 파일을 변형하지 않습니다.

`asset-sources.json`에 출처·크기·SHA-256을 기록했습니다. 앱 원본 및 APK에는 변경을 가하지 않았습니다.

## 운영 정보 설정

`site-config.json`을 수정하고 아래 명령을 실행하면 모든 언어의 HTML에 반영됩니다.

```powershell
python build_site.py
python verify_site.py
```

| 설정 | 입력 내용 |
| --- | --- |
| `developerName` | Play 스토어에 등록할 실제 개발자/사업자명 |
| `supportEmail` | 공개하여 실제로 수신·회신할 이메일 |
| `playStoreUrl` | 공개된 `com.moadoll` Google Play 주소. 현재 미출시이므로 비어 있음 |
| `siteUrl` | 배포된 홈페이지의 HTTPS 주소. 끝에 `/` 포함 |
| `policyEffectiveDate` | 실제 정책 시행일, `YYYY-MM-DD` |
| `supportRetentionDays` | 문의 처리 완료 후 기록을 보관할 실제 일수 |
| `policiesApproved` | 실제 운영과 정책 검토가 완료된 후 `true` |

사용자가 제공한 개발자명 **K-Terang**, 공개 문의 이메일 **greatryuhg@gmail.com**을 설정했습니다. 두 언어의 정책 페이지·고객지원 메일 링크·사이트 하단에 반영됩니다. 정책 시행일과 문의 기록 보관 기간은 아직 미정입니다.

`playStoreUrl`이 비어 있으면 클릭할 수 있는 가짜 다운로드 링크 대신 ‘Google Play 출시 준비 중’을 표시합니다. 연락처가 없으면 메일 접수를 가장하지 않습니다. 이메일이 설정되면 메일 앱으로 직접 보내는 링크가 만들어지며, 이 홈페이지가 서버에 문의를 접수하거나 기기 데이터를 삭제하지는 않습니다.

정책 필수 정보가 완성되지 않으면 정책 페이지에 출시 전 검토본 안내가 남습니다. 이메일만 입력해도 정책이 자동 확정되지는 않습니다.

## GitHub Pages 배포

현재 작업 환경의 GitHub 통신·로컬 `.git` 쓰기 제한 및 연결된 GitHub 앱의 쓰기 권한 오류(403)로 원격 업로드는 완료되지 않았습니다. 일반 PowerShell에서 다음 명령으로 검증·커밋·push를 실행할 수 있습니다. GitHub 로그인 요청이 표시되면 본인 계정으로 인증하세요.

```powershell
powershell -ExecutionPolicy Bypass -File D:\Projects\characterGameHome\push-home.ps1
```

스크립트는 `K-Ternag/moadollHome`의 `main`에 업로드하고 원격 커밋을 대조합니다. 원격에 관련 없는 이력이 생겼으면 덮어쓰지 않고 중단합니다.

1. `K-Ternag/moadollHome` 저장소의 `main` 브랜치에 이 폴더의 파일을 올립니다.
2. 저장소의 **Settings → Pages → Build and deployment → Source → GitHub Actions**를 선택합니다.
3. **Actions → Deploy GitHub Pages → Run workflow**를 실행하거나 `main`에 push합니다.
4. 배포 작업이 완료되면 표시되는 실제 URL을 확인합니다. 이 저장소의 Pages 주소는 `https://k-ternag.github.io/moadollHome/`입니다. 코드 업로드와 사이트 공개는 별도 단계입니다.

포함된 워크플로는 실제 Pages 기본 주소를 받아 `dist/`에 사이트를 만들고 경로 검사를 거쳐 배포합니다. canonical, Open Graph 이미지의 절대 URL, sitemap, robots 및 하위 경로의 404 복귀 링크가 배포 주소에 맞춰집니다. 원본 코드·설정 파일·검증 기록은 배포 아티팩트에서 제외합니다.

별도의 **Check website** 워크플로는 Chromium에서 모바일·데스크톱 화면과 상호작용을 검사하고 스크린샷을 아티팩트로 저장합니다. 이 검사는 배포 작업과 독립적으로 실행되므로 실제 결과를 확인하세요.

브랜치 배포를 선호하면 `siteUrl`을 설정한 후 `python build_site.py`로 생성한 루트 파일들을 커밋하고 Pages에서 **Deploy from a branch → main → /(root)**를 선택할 수도 있습니다. 이 경우 `pages.yml` 자동 배포는 비활성화하세요. `.nojekyll`이 포함되어 있습니다.

공식 배포 절차: [GitHub Pages 사용자 지정 워크플로](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## Google Play 등록에 연결할 주소

실제 배포 주소를 `BASE/`라고 할 때:

| Play 등록 항목 | 주소·정보 |
| --- | --- |
| 개발자 웹사이트 | `BASE/` |
| 개인정보처리방침 | `BASE/privacy.html` |
| 영어 개인정보처리방침 | `BASE/privacy.en.html` |
| 지원 안내 | `BASE/support.html` 및 실제 지원 이메일 |
| 데이터 삭제 안내 | `BASE/delete-account.html` |

현재 모아돌은 계정을 생성하지 않으므로 이 페이지는 탈퇴 기능이 아니라 **로컬 데이터·저장 이미지·백업·문의 기록의 삭제 안내**입니다. 계정 생성이 없는 앱에 서버 계정 삭제를 제공한다고 표시하지 마세요. 추후 로그인·광고·결제 등을 추가하면 정책과 데이터 보안 응답도 변경해야 합니다.

앱 소스에서 확인한 사항:

- `AndroidManifest.xml`: 인터넷·광고 ID·위치·연락처·카메라·마이크 권한 없음. Android 8·9에 한정한 저장소 쓰기 권한 있음.
- `Storage.kt`, 포토카드 저장 흐름: 인형·카드·초안·설정 및 이전 포인트/아이템 기록을 기기에 저장.
- `backup_rules.xml`, `data_extraction_rules.xml`: 데이터베이스·설정을 Android 백업 및 기기 이전에 포함. ‘어떠한 데이터도 기기 밖으로 나가지 않음’이라고 표시하지 않음.
- `ExportFiles.kt`: PNG를 갤러리에 저장하고 사용자 선택에 따라 Android 공유창 사용.
- 현재 의존성 목록에 광고·인증·결제·분석 SDK 없음.
- 현재 앱 코드에서는 개인정보처리방침 링크/본문을 찾지 못함. **출시 앱 안에도 공개된 정책으로 연결되는 경로나 본문을 추가해야 합니다.** 이 홈페이지 작업에서 앱 소스는 수정하지 않았습니다.

Google Play 제출 전에 실제 운영 정보와 정책을 확정하고 `python verify_site.py --release`를 통과시킨 뒤, 공개 URL의 로그인 없는 접근과 출시 AAB의 SDK·권한·데이터 보안 응답을 확인하세요. 이 명령은 설정 누락을 검사하며 스토어 심사 통과를 보장하지 않습니다. 현재는 정책 시행일·문의 기록 보관 기간·정책 확정 여부가 미설정이므로 의도적으로 실패합니다.

사용자가 제공한 광고 판매자 정보를 루트의 `app-ads.txt`에 등록했으며, `build_site.py`가 배포용 `dist/`에도 복사합니다.

```text
google.com, pub-2125537107016631, DIRECT, f08c47fec0942fa0
```

[AdMob 공식 안내](https://support.google.com/admob/answer/9363762?hl=ko)에 따라 파일은 스토어에 등록한 개발자 웹사이트의 도메인 루트에서 제공해야 합니다. 현재 프로젝트 배포 경로인 `https://k-ternag.github.io/moadollHome/app-ads.txt`에만 올리는 것으로는 충분하지 않습니다. `https://k-ternag.github.io/app-ads.txt`에서도 같은 내용을 제공하도록 도메인 루트 사이트에 게시해야 합니다. 이 파일 추가만으로 앱의 광고 SDK 연동이나 AdMob 인증이 완료되는 것은 아닙니다.

확인한 공식 자료:

- [Google Play 사용자 데이터 및 개인정보처리방침 정책](https://support.google.com/googleplay/android-developer/answer/10144311?hl=ko)
- [앱 계정 삭제 요건](https://support.google.com/googleplay/android-developer/answer/13327111?hl=ko)
- [GitHub Pages 접속 데이터 기록](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages#data-collection)
- [Android 앱 데이터 자동 백업](https://developer.android.com/identity/data/autobackup)

## 수정과 검증

- `site_content.py`: 두 언어의 소개·안내·정책 본문
- `build_site.py`: HTML, 운영 정보, 메타데이터 생성
- `styles.css`: 반응형 레이아웃과 인쇄 스타일
- `app.js`: 탭·확대·모바일 메뉴
- `site-config.json`: 실제 운영 설정
- `verify_site.py`: 14개 페이지의 언어·링크·앵커·이미지 경로 검사
- `browser_check.py`: HTTP 프로젝트 하위 경로, 320/390/768/1440/1920px, 탭·키보드·이미지 확대·FAQ·모바일 메뉴·언어 전환·JavaScript 비활성화 검사

생성된 HTML을 직접 바꾸면 다음 생성 때 덮어씁니다. 원본 텍스트와 생성기를 수정하세요. 생성 과정에는 앱 프로젝트나 원본 이미지 폴더가 더 이상 필요하지 않습니다.

```powershell
python build_site.py
python verify_site.py
node --check app.js
# 브라우저 QA가 필요한 환경에서만:
python -m pip install -r requirements-qa.txt
python -m playwright install chromium
python browser_check.py
```

이 작업 환경에서는 Python Playwright가 `WinError 5`, Node 경로의 Chromium 실행이 `spawn EPERM`으로 차단되었습니다. 따라서 실제 브라우저 렌더링·클릭 검증과 스크린샷은 완료되지 않았습니다. 정적 검사와 JS 문법, 배포용 하위 경로 생성은 통과했습니다. 상세 범위는 `verification.json`에 기록합니다.
