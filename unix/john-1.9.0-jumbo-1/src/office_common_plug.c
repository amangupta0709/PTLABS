/*
 * Office 2007-2013 cracker patch for JtR, common code. 2014 by JimF
 * This file takes replicated but common code, shared between the CPU
 * office format, and the GPU office formats, and places it into one
 * common location (with some tiny tweaks, for things like valid).
 */

#include "arch.h"
#include "misc.h"
#include "common.h"
#include "office_common.h"

void *ms_office_common_get_salt(char *ciphertext)
{
	int i, length;
	char *ctcopy = strdup(ciphertext);
	char *keeptr = ctcopy, *p;
	static ms_office_custom_salt *cur_salt;

	if (!cur_salt) cur_salt = mem_alloc_tiny(sizeof(ms_office_custom_salt), MEM_ALIGN_WORD);
	memset(cur_salt, 0, sizeof(*cur_salt));
	ctcopy += FORMAT_TAG_OFFICE_LEN;	/* skip over "$office$*" */
	p = strtokm(ctcopy, "*");
	cur_salt->version = atoi(p);
	p = strtokm(NULL, "*");
	if (cur_salt->version == 2007) {
		cur_salt->verifierHashSize = atoi(p);
		cur_salt->spinCount = 50000;
	}
	else {
		cur_salt->spinCount = atoi(p);
	}
	p = strtokm(NULL, "*");
	cur_salt->keySize = atoi(p);
	p = strtokm(NULL, "*");
	cur_salt->saltSize = atoi(p);
	p = strtokm(NULL, "*");
	for (i = 0; i < cur_salt->saltSize; i++)
		cur_salt->osalt[i] = atoi16[ARCH_INDEX(p[i * 2])] * 16
			+ atoi16[ARCH_INDEX(p[i * 2 + 1])];
	p = strtokm(NULL, "*");
	for (i = 0; i < 16; i++)
		cur_salt->encryptedVerifier[i] = atoi16[ARCH_INDEX(p[i * 2])] * 16
			+ atoi16[ARCH_INDEX(p[i * 2 + 1])];
	p = strtokm(NULL, "*");
	length = strlen(p) / 2;
	for (i = 0; i < length; i++)
		cur_salt->encryptedVerifierHash[i] = atoi16[ARCH_INDEX(p[i * 2])] * 16
			+ atoi16[ARCH_INDEX(p[i * 2 + 1])];
	MEM_FREE(keeptr);
	return (void *)cur_salt;
}

void *ms_office_common_binary(char *ciphertext)
{
	static unsigned int out[4];
	int i, length;
	char *ctcopy = strdup(ciphertext + FORMAT_TAG_OFFICE_LEN);
	char *p, Tmp[16];

	p = strtokm(ctcopy, "*");
	if (atoi(p) != 2007) {
		memset(out, 0, sizeof(out));
		MEM_FREE(ctcopy);
		return out;
	}
	p = strtokm(NULL, "*");
	p = strtokm(NULL, "*");
	p = strtokm(NULL, "*");
	p = strtokm(NULL, "*");
	p = strtokm(NULL, "*");
	p = strtokm(NULL, "*");
	length = strlen(p) / 2;
	for (i = 0; i < length && i < 16; i++)
		Tmp[i] = atoi16[ARCH_INDEX(p[i * 2])] * 16
			+ atoi16[ARCH_INDEX(p[i * 2 + 1])];
	MEM_FREE(ctcopy);
	memcpy(out, Tmp, 16);
	return out;
}

/* a common 'static' valid function. The valid in each of the     */
/* formats, link to one of the external function which calls this */
int ms_office_common_valid(char *ciphertext, struct fmt_main *self)
{
	char *ctcopy, *ptr, *keeptr;
	int res, extra;

	if (strncmp(ciphertext, FORMAT_TAG_OFFICE, FORMAT_TAG_OFFICE_LEN))
		return 0;
	if (!(ctcopy = strdup(ciphertext))) {
		fprintf(stderr, "Memory allocation failed in office format, unable to check if hash is valid!");
		return 0;
	}
	keeptr = ctcopy;
	ctcopy += FORMAT_TAG_OFFICE_LEN;
	if (!(ptr = strtokm(ctcopy, "*")))
		goto error;
	if (strncmp(ptr, "2007", 4) && strncmp(ptr, "2010", 4) && strncmp(ptr, "2013", 4))
		goto error;
	if (!(ptr = strtokm(NULL, "*"))) /* hash size or iterations */
		goto error;
	if (!isdec(ptr)) goto error;
	if (!(ptr = strtokm(NULL, "*")))
		goto error;
	if (strncmp(ptr, "128", 3) && strncmp(ptr, "256", 3)) /* key size */
		goto error;
	if (!(ptr = strtokm(NULL, "*"))) /* salt size */
		goto error;
	if (!isdec(ptr)) goto error;
	res = atoi(ptr);
	if (res != 16) /* can we handle other values? */
		goto error;
	if (!(ptr = strtokm(NULL, "*"))) /* salt */
		goto error;
	if (hexlenl(ptr, &extra) != res * 2 || extra)
		goto error;
	if (!(ptr = strtokm(NULL, "*"))) /* encrypted verifier */
		goto error;
	if (hexlenl(ptr, &extra) != 32 || extra)
		goto error;
	if (!(ptr = strtokm(NULL, "*"))) /* encrypted verifier hash */
		goto error;
	if (!ishexlc(ptr))
		goto error;
	if (strlen(ptr) > 64)
		goto error;
	if ((ptr = strtokm(NULL, "*")))
		goto error;

	MEM_FREE(keeptr);
	return 1;
error:
	MEM_FREE(keeptr);
	return 0;
}

unsigned int ms_office_common_iteration_count(void *salt)
{
	ms_office_custom_salt *my_salt=(ms_office_custom_salt *)salt;

	return (unsigned int)my_salt->spinCount;
}

/*
 * MS Office version (2007, 2010, 2013) as first tunable cost
 */
unsigned int ms_office_common_version(void *salt)
{
	ms_office_custom_salt *my_salt;

	my_salt = salt;
	return (unsigned int) my_salt->version;
}
