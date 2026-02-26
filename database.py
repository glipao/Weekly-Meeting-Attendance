from supabase import create_client, Client

url = "https://dksaewhgdxppriafhrcm.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRrc2Fld2hnZHhwcHJpYWZocmNtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE5MzAzMjEsImV4cCI6MjA4NzUwNjMyMX0.dyXEQSv-IML0ZM_BSoccZ-fIgAM_xGfYp-r60ky1rXk"

supabase: Client = create_client(url, key)
