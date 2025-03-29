# OneAI

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

專案環境變數已經給了範例環境變數檔(template.env)，修改環境變數，並且將檔名重新命(.env)即可使用環境變數檔。以下是修改範例

```sh
PROJECT__NAME="OneAI API"

INIT__EMAIL="oneai@gmail.com"
INIT__USERNAME="sysadmin"
INIT__PASSWORD="sysadmin123"
INIT__FULLNAME="admin"

DATABASE__SERVER=127.0.0.1
DATABASE__PORT=5432
DATABASE__USER=oneAIadmin
DATABASE__PASSWORD=""
DATABASE__DATABASE=""
```

### Installation

該專案因為會啟動PostgreSQL和API server，因此需仰賴docker compose 啟動DB以及ＡＰＩ server。API server 可以直接專案內dockerfile build image。

透過以下指令啟動API和ＤＢ
```sh
docker compose up --build
```


最後前往 [127.0.0.1:8000/docs](127.0.0.1:8000/docs) 應可看到API swagger文件，如果想看到ＵＩ可前往[http://127.0.0.1:8000/static/index.html](http://127.0.0.1:8000/static/index.html)。

## Github
Github: [https://github.com/Iv9614/OneAI](https://github.com/Iv9614/OneAI)
