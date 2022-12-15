import similarity.levenshtein
import similarity.jaro_winkler
# Usando distancia (0 = igual)

def compJaroWink(graph1, graph2, node1, node2):
    return "{:.4f}".format(similarity.jaro_winkler.get_jaro_winkler_distance(graph1.nodes[node1]['name'], graph2.nodes[node2]['name']))


def compLeven(graph1, graph2, node1, node2):
    return "{:.4f}".format(similarity.levenshtein.get_levenshtein_distance(graph1.nodes[node1]['name'], graph2.nodes[node2]['name']))

