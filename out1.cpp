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
void f17(vector<int>& f18, size_t f19, size_t f20) 
{
	if (f19 >= f20) return;
  	size_t v17 = (f19 + f20) / 2;
	f17(f18, f19, v17);
 	f17(f18, v17 + 1, f20);
 	f21(f18, f19, f20, v17);
}
  void f21(vector<int>& f22, size_t f23, size_t f24, size_t f25) 
{
 	if (f23 >= f24 || f25 < f23 || f25 > f24) return;
 	if (f24 == f23 + 1 && f22[f23] > f22[f24]) 
{
 		swap(f22[f23], f22[f24]);
 		return;
}
  	vector<int> v18(&f22[f23], &f22[f23] + (f24 + 1));
 size_t v19 = f23, v20 = 0, v21 = f25 - f23 + 1;
 	while (v19 <= f24) 
{
 		if (v20 > f25 - f23) 
 			f22[v19] = v18[v21++];
 		else if (v21 > f24 - f23) 
{
 			f22[v19] = v18[v20++];
 			f22[v19] = (v18[v20] < v18[v21]) ? v18[v20++] : v18[v21++];
}
 		 ++v19;
}
}
  int main() 
{
 	vector<int> v22(5);
 	v22[0] = 6;
 	v22[1] = 8;
 	v22[2] = 6;
 	v22[3] = 4;
 	v22[4] = 1;
 	int v23 = 0, v24 = v22.size()-1;
 	f17(v22, v23, v24);
 	int v25 = 0;
 	while (v25 < v22.size())
{
 printf("%d ", v22[v25]);
 v25++;
}
 	return 0;
}
