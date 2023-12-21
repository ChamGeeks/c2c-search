from c2c.load import Load


dataset_file = "data/routes.csv"
if __name__ == "__main__":
    offset = 0
    limit = 100
    loader = Load()
    df = loader.load_routes(offset, limit)
    offset = offset + limit    
    df.to_csv(dataset_file, index=False)
    while len(df) > 0:
        df = loader.load_routes(offset, limit)
        offset = offset + limit    
        df.to_csv(dataset_file, mode='a', header=False, index=False)
