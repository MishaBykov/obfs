void quickSort(int arr[], int left, int right) {
    int i = left, j = right;
    int tmp;
    int pivot = arr[(left + right) / 2];

    /* partition */
    while (i <= j) {
        while (arr[i] < pivot)
            i++;
        while (arr[j] > pivot)
            j--;
        if (i <= j) {
            tmp = arr[i];
            arr[i] = arr[j];
            arr[j] = tmp;
            i++;
            j--;
        }
    }

    /* recursion */
    if (left < j)
        quickSort(arr, left, j);
    if (i < right)
        quickSort(arr, i, right);
}

int main()
{
	int a[5];
	a[0] = 6;
	a[1] = 8;
	a[2] = 6;
	a[3] = 4;
	a[4] = 1;
	int b = 0, c = 4;
	quickSort(a, b, c);
	int i = 0;
	while (i < 5){
        printf("%d ", a[i]);
        i++;
    }
	return 0;
}