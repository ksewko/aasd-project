# aasd-project
Projekt realizowany na zajęcia z Agentowych i aktorowych systemów decyzyjnych na Politechnice Warszawskiej w semestrze: 21Z
Temat projektu: Inteligentny system kontrolujący temperaturę w pomieszczeniach dumu mieszkalnego (jednorodzinnego)

uruchamianie prosody:

sudo /etc/init.d/prosody start

dodawanie agenta:

prosodyctl register nazwa_agenta nazwa_virtual_hosta hasło
localhost = domyślny virtual host
nazwa_agenta@nazwa_virtual_hosta = jid agenta

prosodyctl register windows localhost password
prosodyctl register sensors localhost password
