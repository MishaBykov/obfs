void MergeSort(vector<int>& buf, size_t l, size_t r)
{
    //! Условие выхода из рекурсии
    if(l >= r) return;
  
    size_t m = (l + r) / 2;
  
    //! Рекурсивная сортировка полученных массивов
    MergeSort(buf, l, m);
    MergeSort(buf, m+1, r);
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
  
    for (size_t i = l, j = 0, k = m - l + 1; i <= r; ++i) {
        if (j > m - l) {      
            buf[i] = tmp[k++];
        } else if(k > r - l) {
            buf[i] = tmp[j++];
        } else {
            buf[i] = (tmp[j] < tmp[k]) ? tmp[j++] : tmp[k++];
        }
    }
}