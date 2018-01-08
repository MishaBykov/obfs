  void f0(vector<int>& f1, size_t f2, size_t f3, size_t f4) 
{
 	if (f2 >= f3 || f4 < f2 || f4 > f3) return;
 	if (f3 == f2 + 1 && f1[f2] > f1[f3]) 
{
 		swap(f1[f2], f1[f3]);
 		return;
}
  	vector<int> v0(&f1[f2], &f1[f2] + (f3 + 1));
 size_t v1 = f2, v2 = 0, v3 = f4 - f2 + 1;
 	while (v1 <= f3) 
{
 		if (v2 > f4 - f2) 
 			f1[v1] = v0[v3++];
 		else if (v3 > f3 - f2) 
{
 			f1[v1] = v0[v2++];
 			f1[v1] = (v0[v2] < v0[v3]) ? v0[v2++] : v0[v3++];
}
 		 ++v1;
}
}
void f5(vector<int>& f6, size_t f7, size_t f8) 
{
	if (f7 >= f8) return;
  	size_t v4 = (f7 + f8) / 2;
	f5(f6, f7, v4);
 	f5(f6, v4 + 1, f8);
 	f0(f6, f7, f8, v4);
}
void f13(int f14[], int f15, int f16) 
{
 int v13 = f15, v14 = f16;
 int v15;
 int v16 = f14[(f15 + f16) / 2];
 while (v13 <= v14) 
{
 while (f14[v13] < v16) v13++;
 while (f14[v14] > v16) v14--;
 if (v13 <= v14) 
{
 v15 = f14[v13];
 f14[v13] = f14[v14];
 f14[v14] = v15;
 v13++;
 v14--;
}
}
 if (f15 < v14) f13(f14, f15, v14);
 if (v13 < f16) f13(f14, v13, f16);
}
  int main() 
{
 	int v9[5];
 	v9[0] = 6;
 	v9[1] = 8;
 	v9[2] = 6;
 	v9[3] = 4;
 	v9[4] = 1;
 	int v10 = 0, v11 = 4;
 	f13(v9, v10, v11);
 	int v12 = 0;
 	while (v12 < 5)
{
 printf("%d ", v9[v12]);
 v12++;
}
 	return 0;
}
