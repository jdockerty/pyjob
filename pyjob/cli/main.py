from pyjob.search import Search 
import click
import sys

@click.group()
def cli():
    pass

@cli.command()
@click.option('--terms', '-t', required=True, type=str, multiple=True, help='One or more key terms to use for the search, quote the string if using spaces.')
@click.option('--location', '-l', default=None, type=str, help='Location of the job search, e.g. London.')
@click.option('--extended', '-ext', default=False, help='Get the details of the job to provide an extended description.', is_flag=True)
def search(terms, extended, location):
    
    search_terms = list(terms)
    s = Search()
    
    s.set_location(location)