from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

from db import getMarkedMinutes, FIELDS_IN_ORDER, actIDToName
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.cluster import SpectralClustering
import numpy as np


namedFields = FIELDS_IN_ORDER.split(', ')+['answer']

#Data, correct answers
a, b = getMarkedMinutes()

b1 = set([x[0] for x in b])
b2 = {x:actIDToName(x) for x in b1}
b3 = [b2[x[0]] for x in b]

d = [a[i]+(b3[i],) for i in range(len(a))]

df = pd.DataFrame(data=d, columns=namedFields)

del b1, b2, b3, d

print(df)

input()

plt.style.use('dark_background')

pca = PCA(n_components=3)
pt = pca.fit_transform(a)
print('variance', pca.explained_variance_ratio_)
vrat = pca.explained_variance_ratio_
print('eigenvalues?', pca.singular_values_)
#print('vectors', pca.components_)
'''
vectors = pca.components_
for ii, v in enumerate(vectors):
	print('####')
	
	for kkk in range(1):
		vv = 0
		vvv = []
		for i, value in enumerate(v):
			vv += value*a[kkk][i]#*df.loc[0, namedFields[i]]
			vvv += [value]#*df.loc[0, namedFields[i]]
#			vvv += value*df.loc[0, namedFields[i]]
	#		print(f'{value:.3f} * {namedFields[i]}')
			#print(f'{namedFields[i]} > PC{ii}: {value:.4f} * {vrat[ii]:.4f} = {value*vrat[ii]:.4f}') 
			print(f'{namedFields[i]} [{abs(value*vrat[ii]):.5f}] PC{ii}')
			
#		print('@@@@',vv, np.linalg.norm(vvv))
'''

df = pd.DataFrame(data=pt, columns=['PC1', 'PC2', 'PC3'])
print(df)
input()

#exit(0)

colors = ['', 'r', 'g', 'b', 'yellow']

plt.scatter([x[0] for x in pt], [x[1] for x in pt], c=[colors[x[0]] for x in b])

plt.legend(handles = [mpatches.Patch(color=colors[x], label=['', 'A', 'B', 'C', 'D'][x]) for x in range(1, 5)])




clustering = SpectralClustering(n_clusters=4, random_state=0).fit_predict(pt)
print(clustering)

plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter([x[0] for x in pt], [x[1] for x in pt], [x[2] for x in pt], c=[colors[x+1] for x in clustering])
plt.show()
