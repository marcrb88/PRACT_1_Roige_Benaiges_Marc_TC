Pràctica 1 de l'assignatura Tipologia i cicle de vida de les dades.

Integrants del grup:
- Marc Roige
- Eloi Vilella

## Estructura del repositori

- `source/main.py`: script principal que executa el procés complet de scraping i genera el CSV final.
- `source/fetch_list_selenium.py`: obté el llistat d'ofertes i descobreix els enllaços de detall.
- `source/fetch_detail.py`: extreu els camps d'una oferta concreta a partir del HTML de detall.
- `source/export_dataset.py`: exporta el dataset obtingut a format CSV.
- `requirements.txt`: dependències Python necessàries per executar el projecte.
- `dataset/`: carpeta on es desa el dataset resultant en format CSV.

## Requisits previs

1. Tenir Python 3 instal·lat.
2. Tenir Google Chrome o Chromium disponible al sistema perquè Selenium pugui iniciar el navegador.
3. Crear un entorn virtual:

```bash
python -m venv venv
```

4. Activar-lo:

Windows:
```bash
venv\Scripts\activate
```

macOS / Linux:
```bash
source venv/bin/activate
```

5. Instal·lar les dependències:

```bash
pip install -r requirements.txt
```

## Com executar el codi

Des de la carpeta arrel del repositori:

```bash
python source/main.py
```

Quan l'execució finalitza correctament, el dataset es desa a:

```text
dataset/cido_oposicions.csv
```

## Exemple d'ús replicable

```bash
python source/main.py
```

## Dataset i DOI

- Dataset CSV al repositori: `dataset/cido_oposicions.csv`
- DOI de Zenodo: [10.5281/zenodo.19423997](https://doi.org/10.5281/zenodo.19423997)


