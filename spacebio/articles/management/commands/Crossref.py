from django.core.management.base import BaseCommand
from habanero import Crossref
from articles.models import Article
import json
from django.db import transaction, IntegrityError


class Command(BaseCommand):
    help = 'Busca artigos relacionados a "microgravity" e insere no banco de dados'

    def handle(self, *args, **kwargs):
        cr = Crossref()
        query = "Astrobiology"
        results = cr.works(query=query, filter={'has-abstract': True}, limit=100)

        for item in results['message']['items']:
            article_data = {
                    'id': item.get('DOI', ''),
                    'source': item.get('container-title', [''])[0],
                    'pmid': None,  # CrossRef API não retorna PMID
                    'pmcid': None,  # CrossRef API não retorna PMCID
                    'doi': item.get('DOI', ''),
                    'title': item.get('title', [])[0],
                    'author_full_name': ', '.join(
                        [f"{author.get('given', '')} {author.get('family', '')}" for author in item.get('author', [])]
                    ),
                    'author_affiliation_details': ', '.join(
                        [aff.get('name', '') for author in item.get('author', []) for aff in author.get('affiliation', [])]
                    ),
                    'journal_title': item.get('container-title', [''])[0],
                    'journal_issn': item.get('ISSN', [None])[0],
                    'journal_issue': item.get('issue', ''),
                    'journal_volume': item.get('volume', ''),
                    'journal_year_of_publication': item.get('published-print', {}).get('date-parts', [[None]])[0][0],
                    'abstract_text':item.get('abstract', ''),
                    'publication_status': None,  # CrossRef API não retorna status de publicação
                    'language': item.get('language', ''),
                    'pub_model': None,  # CrossRef API não retorna modelo de publicação
                    'pub_type_list': item.get('type', ''),
                    'grants_list': json.dumps(item.get('funder', [])),  # Serializando como JSON para armazenar em TextField
                    'full_text_url_list': ', '.join([link.get('URL', '') for link in item.get('link', [])]),
                }
                # Use update_or_create to avoid duplicate entries
            Article.objects.update_or_create(
                    id=article_data['doi'],
                    defaults=article_data
                )
            self.stdout.write(self.style.SUCCESS(f""))
