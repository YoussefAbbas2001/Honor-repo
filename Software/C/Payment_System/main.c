#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdio.h>
#include <stdlib.h>
#include "STD_TYPES.h"

#include "card.h"



int main()
{
	uint8_t name_validation;

	ST_cardData_t card;
	name_validation = getCardHolderName(&card);
	switch (name_validation)

	{
	case OK:
		printf("%s is valid Name", card.cardHolderName);
		break;
	case WRONG_NAME:
		printf("%s is not a valid name", card.cardHolderName);
		break;
	default:

		break;
	}

}