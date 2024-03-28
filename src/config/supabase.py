from supabase import create_client, Client
from src.config.settings import get_settings

url: str = get_settings().supabase_url
key: str = get_settings().supabase_key
supa: Client = create_client(url, key)