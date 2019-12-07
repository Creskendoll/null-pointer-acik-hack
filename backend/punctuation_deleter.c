#include<stdio.h>
int main(){
	FILE *in=fopen("in.txt", "r");
	FILE *out=fopen("out.txt", "w");
	if(in==NULL){
		printf("Dosya açýlamadý\n");
		return -1;
	}
	char c;
	char state='.'; //  ' ',   '.',   'a'
	int i=0;
	while(1){
		if( fscanf(in, "%c" , &c) == EOF) break;
		
		if(c==' ' || c=='\n' || c=='\r'){
			if(state=='a') state=' ';
		}
		else if(c=='.' || c=='—' || c=='?' || c=='!'){
			if(state!='.'){
				fprintf(out, ".\n");
				state = '.';
			}
		}
		else{ //harf
			if(state==' ')fprintf(out, " ");
			
			state='a';
			
			fprintf(out, "%c",c);
		}
		i++;
		if(i%10000==0)printf("%dk karakter okundu\n",i/1000,c);
	}
	printf("bitti\n");
	fclose(in);
	fclose(out);
	return 0;
}
