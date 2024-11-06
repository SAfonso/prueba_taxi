from pathlib import Path
import pandas as pd

def readAllFiles (rootPath):

    directory = Path(rootPath)
    dataFrames = []

    for f in directory.iterdir():
        if f.suffix =='.parquet':
            df = pd.read_parquet(f)
            dataFrames.append(df)

    df_total = pd.concat(dataFrames, ignore_index=True)

    return df_total

def readFilesFromList (pathList):

    return pd.concat([pd.read_parquet(file) for file in pathList])

def readFile (path):

    return pd.read_parquet(path)


def writeFilterCSV (dataFrame, name, path):

    newPath = Path(path) / name
    dataFrame.to_csv(newPath, index=False)
