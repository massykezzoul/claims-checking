# Rating value system of fatabyyano :

- صحيح --> TRUE
- زائف جزئياً --> MIXTURE
- عنوان مضلل --> OTHER?
- رأي --> OTHER? (Opinion)
- ساخر --> OTHER? (Sarcastique)
- غير مؤهل --> FALSE? (Inéligible)
- خادع --> FALSE? (Trompeur)
- زائف --> FALSE

# Clear cache 
redis-cli --raw keys "https://fatabyyano.net/*" | xargs redis-cli --raw del -
