# Defining the top-tier, medium-tier, and low-tier languages
top_tier_languages = {'python', 'c', 'c++', 'zig', 'rust', 'asm', 'lua'}
medium_tier_languages = {'js', 'ts', 'ruby', 'java', 'jupyter', 'shell', 'php', 'openscad'}
low_tier_languages = {'c#', 'html', 'css'}

# Function to classify the user's grade based on the criteria
def classify_user(row):
    # Extract relevant data from the row
    followers = row['followers']
    stars = row['total_stars']
    forks = row['total_forks']
    watchers = row['total_watchers']
    languages = set(eval(row['languages'].replace('set()', '[]').replace('{', '[').replace('}', ']')))
    
    # Check if the user meets the threshold criteria
    meets_thresholds = {
        'followers': followers >= 20,
        'stars': stars >= 30,
        'forks': forks >= 20,
        'watchers': watchers >= 30
    }
    
    # Count how many thresholds are met
    threshold_count = sum(meets_thresholds.values())
    
    # Check language tier classification
    top_language_count = len(languages & top_tier_languages)
    medium_language_count = len(languages & medium_tier_languages)
    
    # Classify based on the given criteria
    if threshold_count == 4 and top_language_count >= 2:
        return 'Excellent'
    elif threshold_count == 4 and (top_language_count >= 1 or medium_language_count >= 1):
        return 'Good'
    elif threshold_count >= 2 and (top_language_count >= 1 or medium_language_count >= 1):
        return 'Average'
    else:
        return 'Bad'

# Apply classification to the dataset
data['classification'] = data.apply(classify_user, axis=1)

# Display a sample of the results
data[['login', 'followers', 'total_stars', 'total_forks', 'total_watchers', 'languages', 'classification']].head()
