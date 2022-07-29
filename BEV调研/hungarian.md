##### 匈牙利算法----二分图匹配

[趣写算法系列之--匈牙利算法_Dark_Scope的博客-CSDN博客_匈牙利算法](https://blog.csdn.net/dark_scope/article/details/8880547)

```c
int M, N;

int map[MAXM][MAXN];
int p[MAXN];
bool vis[MAXN];
bool match(int i){
    for(int j=1;j<=N;++j){
        if(map[i][j] && !vis[j]){
            vis[j]=true;
            if(p[j]==0 || match(p[j])){
                p[j]=i;
                return true;
            }    
        }
    }
    return false;
}


int hungarian(){
    int cnt=0;
    for(int i=1;i<=M;++i){
        memset(vis, 0, sizeof(vis));
        if(match(i))
            ++cnt;
    }
}
```

##### KM （Kuhn-Munkres）算法

针对 带权重的二分图匹配问题， 如果增加一些约束，是否能更好的实现后处理

```cpp
#include<bits/stdc++.h>
using namespace std;
const int N=205;
int w[N][N];
int la[N],lb[N];
bool va[N],vb[N];
int match[N];
int delta,n;
void read() {
    scanf("%d",&n);
    for(int i=1;i<=n;i++)
        for(int j=1;j<=n;j++)
            scanf("%d",&w[i][j]);
}
bool dfs(int x) {
    va[x]=1;
    for(int y=1;y<=n;y++)
        if(!vb[y])
            if(la[x]+lb[y]-w[x][y]==0) {
                vb[y]=1;
                if(!match[y]||dfs(match[y])) {
                    match[y]=x;
                    return true;
                }
            }
            else
                delta=min(delta,la[x]+lb[y]-w[x][y]);
    return false;
}
int KM() {
    for(int i=1;i<=n;i++) {
        la[i]=-(1<<30);
        lb[i]=0;
        for(int j=1;j<=n;j++)
            la[i]=max(la[i],w[i][j]);
    }
    for(int i=1;i<=n;i++)
        while(true) {
            memset(va,0,sizeof(va));
            memset(vb,0,sizeof(vb));
            delta=1<<30;
            if(dfs(i))
                break;
            for(int j=1;j<=n;j++) {
                if(va[j])
                    la[j]-=delta;
                if(vb[j])
                    lb[j]+=delta;
            }
        }
    int ans=0;
    for(int i=1;i<=n;i++)
        ans+=w[match[i]][i];
    return ans;
}
void write() {
    printf("%d\n",KM());
}
int main() {
    read();
    write();
}
```
