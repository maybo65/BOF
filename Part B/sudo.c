#include <openssl/sha.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define PASSWORD "58945afce4b671b31cd3b047a1c9b1df0bc7a976c67623b2bbf6da6b6028741c"

void sha256(const char* data, char* hash)
{
    int i;
    SHA256_CTX sha256;
    unsigned char buff[SHA256_DIGEST_LENGTH] = {0};

    SHA256_Init(&sha256);
    SHA256_Update(&sha256, data, strlen(data));
    SHA256_Final(buff, &sha256);

    for (i = 0; i < sizeof(buff); i++)
        sprintf(hash + 2*i, "%02x", buff[i]);
}

int check_password(const char* password)
{
    char buff[65] = {0};
    char hash[65] = {0};

    buff[0]  = 'T';
    buff[1]  = 'h';
    buff[2]  = 'i';
    buff[3]  = 's';
    buff[4]  = 'i';
    buff[5]  = 's';
    buff[6]  = 's';
    buff[7]  = 'a';
    buff[8]  = 'l';
    buff[9]  = 't';
    buff[10] = '\0';
    strcat(buff, password);
    sha256(buff, hash);

    return strcmp(hash, PASSWORD) == 0;
}

int main(int argc, char* argv[])
{
    setuid(0);
    setgid(0);

    if (argc < 3) {
        printf("USAGE: %s <password> <command>\n", argv[0]);
        return 1;
    }

    if (check_password(argv[1])) {
        printf("Running command...\n");
        fflush(stdout);
        system(argv[2]);
    }
    else {
        printf("ERROR: invalid password.\n");
        return 1;
    }

    return 0;
}
