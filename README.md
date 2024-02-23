# Make The Pix

![showcase](https://raw.githubusercontent.com/mKsDEV08/makethepix/master/images/makethepix_showcase.gif)

## Roadmap 🗺️

- ✅ Criação do serviço de alertas.
    - ✅ Implementação do módulo de voz.
    - ✅ Implementação de um Queue de doações.
- 🚧 Criação do serviço de cadastro.
- 🚧 Criação da dashboard do usuário.
- 🚧 Criação da integração de pagamento.
- 🚧 Criação do gateway de doação.
- 🚧 Lançamento (data prevista 04/2024).

## Installation

Cloning repo

```cli
git clone https://github.com/mKsDEV08/makethepix.git
```

Creating Python virtual enviroment

```cli
python3 -m venv .venv
source .venv/bin/activate
```

Setting-up database

```sql
CREATE DATABASE makethepix;
USE makethepix;
```
```sql
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(16) NOT NULL,
  `password_hash` varchar(162) NOT NULL,
  `alert_id` varchar(24) NOT NULL,
  `balance` double NOT NULL,
  `lang_choose` varchar(6) DEFAULT 'com.br',
  `pix_key` text NOT NULL,
  `pitch_choose` double NOT NULL,
  PRIMARY KEY (`id`)
);
```
```sql
CREATE TABLE `messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `message` varchar(300) NOT NULL,
  `sender_name` varchar(16) NOT NULL,
  `status` varchar(8) DEFAULT 'pending',
  `value` double NOT NULL,
  `receiver_alert_id` varchar(24) NOT NULL,
  PRIMARY KEY (`id`)
);
```

### alert-server

Installing `alert-server` dependencies

```cli
cd alert-server
pip install -r requirements.txt
```

Change MySQL credentials on `helpers.py`
![db_change](https://raw.githubusercontent.com/mKsDEV08/makethepix/master/images/database_change.gif)

Starting `alert-server`

```cli
python wsig.py
```
