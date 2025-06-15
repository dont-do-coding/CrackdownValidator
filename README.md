## 📄 데이터 번들 파일(`.g2b`) 생성 및 구조 문서화

`.g2b` 파일은 일반적으로 **GZIP 압축된 TAR 아카이브**이며, 특정 구조를 가진 데이터와 이미지들을 하나의 파일로 묶어 관리하기 위한 목적으로 사용됩니다.

이 문서에서는 `.g2b` 파일을 생성하고 읽는 방법을 설명합니다.

만약에, `.g2b` 파일로 만드는 것이 어렵다면, 폴더 형식으로 입력하는 방법도 있습니다.

---

### 📌 1. 파일 및 폴더 구조 예시

기본적으로 아래와 같은 폴더 구조를 가집니다.

```
data/
├── data.yml
└── img/
    ├── 250517072420_250517072420_28_19_3554448_16_1.jpg
    ├── 250517072420_250517072434_28_19_3554448_16_2.jpg
    ├── ...
```

* `_data` 폴더는 모든 구성요소(`data.yml` 및 이미지 파일)를 포함하는 최상위 디렉터리입니다.
* YAML 파일(`data.yml`)에는 데이터 메타 정보 및 이미지 경로 목록이 저장됩니다.

---

### 📌 2. `.g2b` 파일 생성 방법

`.g2b` 파일은 **GZIP 압축 방식의 TAR 파일**입니다. 이를 생성하기 위해 일반적으로 사용하는 명령어는 다음과 같습니다.

```bash
tar -zcf ./data.g2b -C ./data .
```

* `-z`: gzip 압축을 사용합니다.
* `-c`: 새 아카이브를 생성합니다.
* `-f`: 아카이브 파일 이름을 지정합니다.
* `-C ./_data`: 아카이브 생성 전에 `_data` 폴더로 이동하여, 아카이브 내부에서 경로가 최상위 폴더 없이 바로 나오도록 합니다.
* 마지막 `.`(점)은 `_data` 내부의 모든 내용을 포함하라는 의미입니다.

결과적으로 아카이브 내부 구조는 다음과 같이 됩니다:

```
data.yml
img/
└── *.jpg
```

---

### 📌 3. `.g2b` 파일 읽기 및 활용 (Python 코드 설명)

제공된 Python 코드의 주요 목적은 다음과 같습니다.

**주요 작업**:

* `.g2b` 파일을 읽어들입니다.
* 내부의 `data.yml` YAML 파일을 추출하여 메타 데이터를 파싱합니다.
* 이미지 파일을 순서대로 읽고, SHA-256과 MD5 해시를 계산하여 이미지 무결성을 확인합니다.

### 🧑‍💻 코드 단계별 설명:

1. **라이브러리 불러오기**

```python
import tarfile
import yaml
import hashlib
```

2. **파일 열기**

```python
tar_path = 'data.g2b'

with tarfile.open(tar_path, mode='r:gz') as tar:
```

* `.g2b`는 gzip 압축이므로, `r:gz` 모드를 사용하여 엽니다.

3. **`data.yml` 파일 파싱**

```python
member = tar.getmember('./data.yml')
f = tar.extractfile(member)
content = f.read().decode('utf-8')
yaml_data = yaml.safe_load(content)
```

* YAML 파일을 읽어 Python 딕셔너리로 변환합니다.

4. **YAML 내용 출력**

```python
print(f"--- YAML Data ---")
print('Secret Token : ' + yaml_data['secret']['token'])
print('Company Code : ' + str(yaml_data['base']['company_code']))
print('Company Name : ' + yaml_data['base']['company_name'])
print('Confirm Code : ' + str(yaml_data['base']['confirm_code']))
print('Crackdown Level : ' + str(yaml_data['base']['crackdown_level']))
print('Start Time : ' + yaml_data['base']['start_time'])
print('End Time : ' + yaml_data['base']['end_time'])
print('Place Name : ' + yaml_data['base']['place_name'])
print('Plate Text : ' + yaml_data['base']['plate_text'])
print('Zone : ' + str(yaml_data['base']['zone']))
print('Image Count : ' + str(len(yaml_data['image'])))
```

* YAML 파일의 내용을 상세히 출력하여 내용을 확인할 수 있습니다.

5. **이미지 파일 읽기 및 해시 계산**

```python
for i in range(len(yaml_data['image'])):
    member = tar.getmember(yaml_data['image'][i]['image_path'])
    f = tar.extractfile(member)
    content = f.read()
    sha256_hash = hashlib.sha256(content).hexdigest()
    md5_hash = hashlib.md5(content).hexdigest()

    print(f"--- image {i:04} ---")
    print('Capture Time : ' + yaml_data['image'][i]['capture_time'])
    print('Crackdown Level : ' + str(yaml_data['image'][i]['crackdown_level']))
    print('Image Level: ' + str(yaml_data['image'][i]['image_level']))
    print('Image Path : ' + yaml_data['image'][i]['image_path'])
    print('Image Size : ' + str(len(content)))
    print(f"SHA256: {sha256_hash}")
    print(f"MD5: {md5_hash}")
```

* 이미지 파일을 읽고, SHA-256 및 MD5 해시를 계산하여 이미지 파일의 정확성과 무결성을 검증하세요.

---

### ✅ 최종 정리

| 항목    | 설명                                             |
| ----- | ---------------------------------------------- |
| 확장자   | `.g2b` (실질적으로는 gzip 압축 TAR 형식)                 |
| 생성 방법 | `tar -zcf ./data.g2b -C ./_data .`             |
| 주요 내용 | YAML 메타 데이터 (`data.yml`), 이미지 또는 기타 데이터        |
| 해시 검증 | SHA-256 및 MD5를 통해 무결성 검증 가능                    |
| 파싱 도구 | Python에서 `tarfile`, `yaml`, `hashlib` 라이브러리 사용 |
