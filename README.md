# MoaDoll · 모아돌 홈페이지

GitHub Pages용 한국어·영어 정적 홈페이지입니다. `D:\Projects\foutFoldHome`의 다국어·정책·지원 페이지 구성을 참고하고, 모아돌의 실제 기능과 제공된 이미지에 맞춰 새로 제작했습니다.

- 한국어: [index.html](index.html)
- 영어: [index.en.html](index.en.html)
- 사이트 폴더: `D:\Projects\characterGameHome`
- 개인정보 처리 확인 기준: `com.moadoll`, `0.15.18-app-update`, versionCode 62 (2026-11-17 소스 및 생성된 release 병합 Manifest 확인)
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
| `delete-account.html` | 기기 데이터·이미지·파일/Drive/시스템 백업·구매 기록·문의 기록 삭제 안내 |
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
| `supportDeletionMethod` | 문의 이메일·첨부파일 삭제 방법, `ko`/`en` 문구 |
| `targetAudience` | 실제 이용 대상 연령, `ko`/`en` 문구 |
| `childrenPrivacyPolicy` | 아동 대상 광고·동의 처리 방식, `ko`/`en` 문구 |
| `externalProcessingDetails` | 제공업체의 보관·국외 처리 추가 고지, `ko`/`en` 문구 |
| `policiesApproved` | 실제 운영과 정책 검토가 완료된 후 `true` |

2026-11-17 사용자 확인에 따라 운영자 **K-Terang**, 공개 문의 이메일 **greatryuhg@gmail.com**, 정책 시행일 **2026-11-17**, 이용 대상 **전체 연령(아동 포함)**을 설정했습니다. 문의 이메일과 첨부파일은 사용자가 위임한 운영 방침에 따라 **문의 처리 완료 후 30일** 보관한 뒤 운영자가 메일함·휴지통에서 영구 삭제하고, 문제 해결을 위해 별도 저장한 첨부파일 사본도 삭제하도록 정했습니다. 확인된 삭제 요청도 같은 방법으로 처리합니다. 이는 운영자가 실행할 방침이며 홈페이지에 메일 자동 삭제 기능을 구현한 것은 아닙니다.

아동 대상 광고·동의 처리 방식과 외부 제공업체의 보관·국외 처리 추가 고지는 미정입니다. 해당 두 설정의 양쪽 언어를 채우고 실제 운영·앱 설정을 확인한 뒤 `policiesApproved`를 `true`로 바꾸세요. 모든 필수 값이 갖춰지면 생성기가 상단 검토본 안내와 ‘확정 예정’ 표시를 제거합니다. 설정 누락 상태에서 `true`를 지정하면 빌드가 실패합니다. 확정된 시행일만으로 정책 최종 검토가 완료된 것은 아닙니다.

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

모아돌 자체 회원가입은 없으며, Google 인증은 선택적 Drive 백업·복원에 사용됩니다. 삭제 안내는 **기기 데이터·저장 이미지·파일/Drive/시스템 백업·구매 기록·문의 기록**을 구분합니다. 앱 삭제나 Google 연결 해제가 모든 외부 백업·구매 기록의 삭제를 뜻하지 않습니다.

앱 소스에서 확인한 사항:

- `app/build.gradle.kts`: Google Mobile Ads `25.5.0`, UMP `4.0.0`, Play Billing `8.3.0`, Google auth `22.0.0` 사용.
- `AndroidManifest.xml` 및 release 병합 Manifest: 인터넷·네트워크 상태·Play 결제·광고 ID·광고 서비스 권한, Android 8·9 저장소 쓰기 권한 포함. 위치·연락처·카메라·마이크 권한 없음. SDK가 병합한 기타 일반 권한은 최종 AAB에서도 확인.
- `RewardedAds.kt`, `FullscreenAds.kt`: 배너·전면·보상형 광고, UMP 동의/개인정보 선택, 전체 이용권 보유 시 광고 요청·표시 제한. UMP 호출만으로 아동 대상 처리까지 완료되었다고 판단하지 않음.
- `PlayPurchases.kt`, `CommerceStore.kt`: 상품·구매 토큰·구매 상태·서명 검증, 구매 승인 및 로컬 이용권 기록. 카드번호·은행 계좌정보 직접 수집 없음.
- `LocalBackup.kt`, `BackupRewards.kt`: 사용자가 선택한 인형·카드·문구·보유 아이템·당일 보상 기록의 수동 백업. PNG·코인 잔액·이용권 구매정보 제외.
- `DriveBackup.kt`, `DriveBackupController.kt`, `CommerceScreens.kt`: `drive.appdata` 권한만 요청. 사용자 Drive의 `appDataFolder`에 저장하며 접근 토큰은 메모리에서 사용. 업로드 내용을 다시 읽어 검증한 후 최신 1개를 남기도록 정리하고, 정리 실패 시 이전 파일이 남을 수 있음. 현재 백업 목록 UI는 복원·새로고침을 제공하므로 존재하지 않는 앱 내 삭제 버튼을 안내하지 않음.
- `WeatherData.kt`, `WeatherController.kt`: WeatherAPI에 기본/선택 도시 좌표와 검색어 전송. 기기 GPS 사용 없음. 선택 도시·검색·날씨 결과 기기 저장. 날씨 1시간·검색 24시간은 캐시 재사용 기준이며 시간 경과 후 자동 삭제 코드가 아님.
- `backup_rules.xml`, `data_extraction_rules.xml`: 데이터베이스와 `file/datastore/`를 Android 백업 및 기기 이전에 포함. 수동 백업의 제외 규칙을 시스템 백업에 그대로 적용하지 않음.
- `ExportFiles.kt`: PNG를 갤러리에 저장하고 사용자 선택에 따라 Android 공유창 사용.
- `CommerceScreens.kt`: 앱 내 개인정보처리방침 열기 기능 확인. 이번 작업에서는 홈페이지 소스만 변경하며 앱·APK·AAB를 수정하거나 다시 빌드하지 않음.

Google Play 제출 전에 실제 운영 정보와 정책을 확정하고 `python verify_site.py --release`를 통과시킨 뒤, 공개 URL의 로그인 없는 접근과 출시 AAB의 SDK·권한·데이터 보안 응답을 확인하세요. 이 명령은 설정 누락을 검사하며 스토어 심사 통과를 보장하지 않습니다. 현재는 `childrenPrivacyPolicy`, `externalProcessingDetails`, `policiesApproved`가 미확정이므로 의도적으로 실패합니다.

### Play Console 데이터 보안 대조표

아래는 이번 정책 수정과 맞춘 **신고 준비 자료**입니다. Play Console의 실제 신고를 조회·변경·제출한 것은 아닙니다. 개발자 서버가 없다는 이유로 ‘수집/공유 없음’을 선택할 수 없으며, SDK가 외부로 보내는 정보도 검토해야 합니다. [Google 데이터 보안 안내](https://support.google.com/googleplay/android-developer/answer/10787469?hl=ko), [사용자 데이터 정책](https://support.google.com/googleplay/android-developer/answer/10144311?hl=ko).

| 기능·근거 | 검토할 데이터 유형 / English label | 처리·목적 및 신고 판단 |
| --- | --- | --- |
| AdMob IP 주소 | 대략적인 위치 / Approximate location | IP로 대략적인 위치가 추정될 수 있음. 광고·성과 측정·부정 이용 방지. GPS 권한이 없다는 이유로 이 항목을 제외하지 않음. |
| AdMob 광고 ID·앱 세트 ID 등 | 기기 또는 기타 ID / Device or other IDs | 광고 SDK의 수집·공유 반영. 실제 적용되는 계정 관련 식별정보도 공식 SDK 설명과 대조. |
| AdMob 앱 실행·탭·영상 조회 | 앱 상호작용 / App interactions | SDK의 수집·공유, 광고·분석 목적 검토. |
| AdMob 앱·SDK 성능 정보 | 진단 / Diagnostics, 기타 앱 성능 데이터 / Other app performance data | 실제 버전의 보고 항목을 Console 유형에 대응. 공식 설명만으로 확인되지 않은 별도 crash 수집을 단정하지 않음. |
| Google Play 전체 이용권 | 구매 내역 / Purchase history | 상품·토큰·상태·서명된 구매정보의 확인·승인·복원 경로를 기준으로 앱 기능 및 부정 이용 방지 목적 검토. 외부 결제 화면에서만 받는 카드번호·은행 정보와 앱이 직접 처리하는 구매정보를 구분. |
| Drive 수동 백업 | 기타 사용자 제작 콘텐츠 / Other user-generated content, 기타 활동 / Other actions 등 | 인형·카드·문구·보유 아이템·당일 보상 기록을 선택적으로 외부 전송함. 앱이 백업 데이터를 생성하고 읽으므로 ‘앱이 데이터를 전혀 접근하지 않는 외부 저장’ 예외를 그대로 적용하지 않음. 사용자 선택에 따른 전송의 공유 예외는 실제 고지·동작으로 별도 검토. |
| Google Drive 인증 | 사용자 ID / User IDs 등 해당 항목 검토 | 현재 앱은 `drive.appdata` 인증 토큰을 Drive 요청에 사용. Google 계정 인증이 있다는 이유만으로 앱이 이름·이메일을 별도 수집한다고 단정하지 않음. 실제 SDK 전송과 최종 빌드 확인. |
| WeatherAPI 도시 검색·날씨 | 앱 내 검색 기록 / In-app search history, 위치 관련 항목 검토 | 검색어·기본/선택 도시 좌표·접속 IP 처리. 기능 제공 목적. 선택 도시 좌표를 기기 GPS 정밀 위치 수집으로 오인하지 않도록 실제 위치 추론 여부와 제공자 처리를 확인. |
| 기기 편집 데이터·PNG·파일 백업 | 기기 내부 처리와 외부 전송을 구분 | 기기 내부 처리만 있는 데이터와 공유·Drive 등 외부 전송 기능을 분리해서 판단. 백업 파일을 다른 클라우드 저장 위치로 내보내는 경우도 확인. |
| 이메일 문의 | 이메일 주소 / Email address, 이메일 / Emails, 첨부 내용에 해당하는 유형 | 문의 회신·문제 해결. 웹사이트 문의는 정책에 공개하되 앱의 신고 범위는 실제 문의 진입·전송 경로에 맞춰 확인. 처리 완료 후 30일, 메일함·휴지통·별도 첨부 사본 삭제. |

[AdMob 공식 공개 자료](https://developers.google.com/admob/android/privacy/play-data-disclosure)는 확인한 앱의 SDK `25.5.0`과 일치합니다. 광고의 각 유형별 수집·공유 여부와 목적을 검토하고, 전체 이용권의 광고 중단을 전체 사용자에 대한 ‘수집 없음’으로 일반화하지 마세요. 광고 ID 삭제나 비개인화 선택이 모든 광고 데이터를 차단하는 것도 아닙니다.

각 데이터 유형에 대해 실제 **수집·공유, 필수·선택, 목적, 임시 처리 여부**를 확정해야 합니다. Drive/날씨처럼 선택 기능인 경우에도 기기 밖 처리가 있다면 범위에 포함합니다. 로컬 캐시의 1시간·24시간을 외부 서버 보관기간이나 일시적 처리의 증거로 사용하지 않습니다. HTTPS/TLS는 확인한 Drive·WeatherAPI 요청과 AdMob 공식 설명에 근거하며, 모든 전송 암호화 응답은 최종 AAB의 SDK·외부 전송 경로까지 확인 후 확정합니다. 지원 이메일로 요청할 수 있는 문의 기록과 사용자가 직접 삭제하는 기기/외부 데이터를 구분하여 삭제 관련 질문에 답하세요.

### 최종 확정에 남은 운영 항목

- **아동 포함 전체 연령:** 사용자 의도를 전체 연령 대상으로 기록했습니다. 콘텐츠 등급 ‘전체이용가’와 Play Console 대상 연령 그룹은 별도 항목입니다. 연령별 광고 처리, 연령 미확인 사용자 처리, 맞춤 광고 제한, 동의 및 필요한 보호자 절차, SDK/AdMob 설정을 정한 뒤 실제 앱과 정책을 함께 맞춰야 합니다. 현재 확인한 코드에는 UMP 흐름은 있으나 명시적인 아동 대상 광고 설정을 확인하지 못했습니다. 이 홈페이지 변경으로 앱의 아동 광고 처리가 구현되는 것은 아닙니다. [Google Play Families 정책](https://support.google.com/googleplay/android-developer/answer/9893335?hl=ko), [AdMob 타기팅 설정](https://developers.google.com/admob/android/targeting).
- **제공업체의 보관·국외 처리:** 적용 국가, 계약상 수신 법인·처리 국가, 항목·목적·이전 시점/방법, 보관기간 및 권리 행사 경로 중 추가로 고지할 사항을 실제 계약과 서비스 설정으로 확정해야 합니다. WeatherAPI는 Zoomash Ltd 서비스이며, API 입력 데이터 처리는 해당 계약/DPA 범위도 확인합니다. 개발자용 WeatherAPI 계정·결제 보관기간을 모아돌 사용자 날씨 데이터의 보관기간으로 옮겨 적지 마세요. [WeatherAPI 개인정보처리방침](https://www.weatherapi.com/privacy), [Google 개인정보처리방침](https://policies.google.com/privacy).
- **Google API 사용자 데이터 정책:** `drive.appdata` 최소 권한과 백업·복원 목적의 사용을 유지하고, 공개 정책과 OAuth 설정도 같은 처리 내용으로 맞추세요. 미확정 준수 사항을 완료했다고 표시하지 않습니다. [Google API Services User Data Policy](https://developers.google.com/terms/api-services-user-data-policy), [Drive 앱 전용 데이터](https://developers.google.com/workspace/drive/api/guides/appdata).

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

2026-11-17 정책 변경 후 14개 페이지·378개 로컬 참조, 두 언어의 정책 섹션 수, 생성 결과와 원본/설정의 일치, 미완성 정책 승인 차단, 완성 설정에서 검토본·미정 문구 제거, 운영 문구 HTML 이스케이프를 확인했습니다. 배포용 하위 경로 생성과 정적 검사도 통과했습니다. `python browser_check.py`는 현재 환경에 Playwright가 없어 실행되지 않았으므로 브라우저 렌더링·클릭과 스크린샷은 이번 작업에서 검증하지 않았습니다. 상세 범위는 `verification.json`에 기록합니다. 원격 업로드·배포 및 실제 Play Console 신고 제출은 수행하지 않았습니다.
