import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://nepdretnayqeaszqdccg.supabase.co'
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5lcGRyZXRuYXlxZWFzenFkY2NnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIxMDY0OTUsImV4cCI6MjA2NzY4MjQ5NX0.lNKdYvfYnXYvtN7YPImnghEmjuJvO7xuuaZ1wcoQG1I'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

