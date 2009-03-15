class CountryCodes:
    '''
    This is just a helper to generate useful data files. It isn't directly used
    in these examples.
    '''
    
    def __init__(self):
        self.parse_codes_data()   
        
    def parse_codes_data(self):
        lines = open('iso3166-1-a2.txt', 'rb').read().split('\n')
        self.codes = dict([ a.split(' ', 1) for a in lines[:-1] ])

    def get_country_code_from_name(self, guess_name):
        best_score = 100
        best_code = None
        for code, name in self.codes.items():
            score = self.levenshtein(guess_name, name)
            if score < best_score:
                best_score = score
                best_code = code
        return best_code

    def levenshtein(self, a, b):
        "Calculates the Levenshtein distance between a and b."
        n, m = len(a), len(b)
        if n > m:
            # Make sure n <= m, to use O(min(n,m)) space
            a,b = b,a
            n,m = m,n
            
        current = range(n+1)
        for i in range(1,m+1):
            previous, current = current, [i]+[0]*n
            for j in range(1,n+1):
                add, delete = previous[j]+1, current[j-1]+1
                change = previous[j-1]
                if a[j-1] != b[i-1]:
                    change = change + 1
                current[j] = min(add, delete, change)
                
        return current[n]

