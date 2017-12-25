void MergeSort(vector<int>& buf, size_t l, size_t r)
{
	//! Условие выхода из рекурсии
	if (l >= r) return;

	size_t m = (l + r) / 2;

	//! Рекурсивная сортировка полученных массивов
	MergeSort(buf, l, m);
	MergeSort(buf, m + 1, r);
	merge(buf, l, r, m);
}

void merge(vector<int>& buf, size_t l, size_t r, size_t m)
{
	if (l >= r || m < l || m > r) return;
	if (r == l + 1 && buf[l] > buf[r]) {
		swap(buf[l], buf[r]);
		return;
	}

	vector<int> tmp(&buf[l], &buf[l] + (r + 1));
    size_t i = l, j = 0, k = m - l + 1;
	while (i <= r) {
		if (j > m - l) {
			buf[i] = tmp[k++];
		}
		else if (k > r - l) {
			buf[i] = tmp[j++];
		}
		else {
			buf[i] = (tmp[j] < tmp[k]) ? tmp[j++] : tmp[k++];
		}
		 ++i;
	}
}

int main()
{
	vector<int> a(5);
	a[0] = 6;
	a[1] = 8;
	a[2] = 6;
	a[3] = 4;
	a[4] = 1;
	int b = 0, c = a.size()-1;
	MergeSort(a, b, c);
	int i = 0;
	while (i < a.size()){
        printf("%d ", a[i]);
        i++;
    }
	return 0;
}
