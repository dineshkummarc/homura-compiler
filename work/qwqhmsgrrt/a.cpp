#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <algorithm>
using namespace std;

#define f first
#define s second

#define ll long long

int n,m;
pair<int,int> a[4000];
pair<int,int> b[4000];

ll x[4000][4000];
bool e[4000];
int z[4000];

int main(){
	ifstream in("evacuation.in");
	ofstream out("evacuation.out");

	in>>n;
	for (int i=0;i<n;++i) in>>a[i].f, a[i].s = i;
	in>>m;
	for (int i=0;i<m;++i) in>>b[i].f, b[i].s = i;

	sort(a, a+n);
	sort(b, b+m);

	for (int j=0;j<n;++j)
		for (int i=0;i<m;++i) x[i][j] = ((ll)1)<<60;

	for (int j=0;j<n;++j)
		x[0][j] = abs(b[0].f - a[j].f);

	for (int i=1;i<m;++i){
		x[i][i] = abs(b[i].f - a[i].f) + x[i-1][i-1];
		ll q = x[i-1][i-1];
		for (int j=i+1;j<n;++j){
			q = min(q, x[i-1][j-1]);
			x[i][j] = abs(b[i].f - a[j].f) + q;
		}
	}

	/*
	for (int i=0;i<m;++i){
		for (int j=0;j<n;++j) cout<<x[i][j]<<" ";
		cout<<endl;
	}
	*/

	for (int i=m-1;i>=0;--i){
		int t = 0;
		for (;t<n;++t)if (!e[t])break;
		for (int j=0;j<n;++j)
			if (!e[j] && x[i][j] < x[i][t]) t = j;
		e[t] = 1;
		z[t] = i;
		//cout<<i<<" "<<t<<" "<<x[i][t]<<endl;
	}

	ll ans = 0;
	for (int i=0;i<n;++i){
		if (!e[i]){
			z[i] = 0;
			for (int j=0;j<m;++j)
				if (abs(a[i].f-b[j].f) < abs(a[i].f - b[z[i]].f)) z[i] = j;
		}
		ans += abs(a[i].f - b[z[i]].f);
	}

	out<<ans<<endl;
	for (int i=0;i<n;++i)
		out<<b[z[a[i].s]].s+1<<" ";
	out<<endl;

	return 0;
}

