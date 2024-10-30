# KNYGIS

<img src="knygis/data/knygis_logo.jpg" alt="Knygis" width="800"/>

**Kny**gyno **I**nformacinė **S**istema - paprasta bibliotekos valdymo programa


## Turinys

- [Įžanga](#įžanga)
- [Paleidimas](#paleidimas)
- [Funkcijos](#funkcijos)
- [Pakeitimai](#changelog)

## Įžanga

Šio projekto tikslas sukurti nesudėtingą bibliotekos valdymo programą naudojant Python. Ši programa skirta bibliotekos valdymui, suteikianti galimybę tiek skaitytojams, tiek bibliotekininkams atlikti įvairias funkcijas.

## Paleidimas

Iš projekto šakninės direktorijos aktyvuokite virtualią aplinką ir paleiskite `main.py` failiuką su `poetry`
```sh
poetry shell
streamlit run knygis/main.py
```

## Funkcijos
### Prisijungimas

Programoje yra prisijungimo langas, kuriame vartotojai gali pasirinkti:
- *Skaitytojo puslapis*: Skaitytojai gali prisijungti įvedę savo skaitytojo kortelės numerį.
- *Bibliotekininko puslapis*: Bibliotekininkai gali prisijungti naudodami savo vartotojo vardą ir slaptažodį.

### Skaitytojo funkcijos:
- *Peržiūrėti knygas*: Peržiūrėti visų bibliotekos knygų sąrašą, surūšiuoti jų atvaizdavimą pagal įvairius kriterijus.
- *Pasiimti knygą*: Pasiimti knygą, jei neturi neatiduotų ir vėluojančių knygų.
- *Grąžinti knygą*: Pasirinkti iš sąrašo savo turimų knygų ir grąžinti norimą knygą.
- *Ieškoti knygų*: Ieškoti knygų pagal pavadinimą ar autorių.
- *Peržiūrėti savo knygas*:  Peržiūrėti savo paimtas knygas, kada jos buvo paimtos ir grąžintos.
- *Atsijungti*: Baigti sesiją.

### Bibliotekininko funkcijos:
- *Pridėti knygą*: Įvesti norimą kiekį naujų knygų. Jei knyga jau egzistuoja, jos kiekis bus atnaujintas.
- *Pašalinti knygas*: Pašalinti knygas, kurių leidimo data senesnė nei pasirinkta, arba pašalinti knygas pagal knygos ID.
- *Peržiūrėti knygas*: Matyti visą bibliotekos knygų sąrašą.
- *Pridėti skaitytoją*: Įvesti vartotojo vardą ir paspausti 'pridėti'. Skaitytojo kortelės kodas bus sugeneruotas automatiškai ir parodytas ekrane.
- *Peržiūrėti skaitytojus*: Rodyti visus skaitytojus ir jų skaitytojo kortelės kodus.
- *Peržiūrėti vėluojančias knygas*: Matyti, kurios knygos vėluoja, ir kurie vartotojai turi vėluojančių knygų.
- *Inicializuoti duomenis*: Galimybė įkelti iš anksto numatytus duomenis, jei tai dar nebuvo atlikta.
- *Atsijungti*: Baigti sesiją.

## Pakeitimai

Detalus pakeitimų sąrašas (EN) [Changelog](CHANGELOG.md).