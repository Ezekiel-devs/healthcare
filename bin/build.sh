#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

echo "Creating superuser..."
# Cette commande utilise les variables d'environnement pour créer l'utilisateur
# Le || true à la fin est une sécurité : si l'utilisateur existe déjà, la commande échouera
# mais le "|| true" empêchera le build de planter.
python manage.py createsuperuser --noinput || true