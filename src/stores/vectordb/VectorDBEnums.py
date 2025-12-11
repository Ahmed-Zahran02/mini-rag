from enum import Enum


class VectorDBType(Enum):
    CHROMA = "chroma"
    QDRANT = "qdrant"


class DistanceMetric(Enum):
    COSINE = "cosine"
    EUCLIDEAN = "euclidean"
    DOT_PRODUCT = "dot_product"
