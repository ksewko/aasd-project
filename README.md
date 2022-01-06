# aasd-project
Projekt realizowany na zajęcia z Agentowych i Aktorowych Systemów Decyzyjnych na Politechnice Warszawskiej w semestrze: 21Z

Temat projektu: Inteligentny system kontrolujący temperaturę w pomieszczeniach dumu mieszkalnego (jednorodzinnego). System agentowy opiera się na bibliotece SPADE 'https://spade-mas.readthedocs.io/en/latest/readme.html' Zastosowany serwer XMPP: prosody 'https://prosody.im/'.
  
Uruchamianie prosody:
  
sudo /etc/init.d/prosody start
  
Dodawanie agenta:  
  
prosodyctl register nazwa_agenta nazwa_virtual_hosta hasło  
localhost = domyślny virtual host  
nazwa_agenta@nazwa_virtual_hosta = jid agenta  
  
prosodyctl register windows localhost password  
prosodyctl register sensors localhost password  
