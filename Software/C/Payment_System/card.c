#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "STD_TYPES.h"
#include "card.h"

EN_cardError_t getCardHolderName(ST_cardData_t* cardData)
{
    char name[25] = {0};
    printf("Enter Holder Name : ");
    gets(name);
    strcpy(cardData->cardHolderName, name);
    if ((name == NULL) || (strlen(name) > 24) || (strlen(name) < 20))
        // Check that name length in range [20,24]
        return WRONG_NAME;

    else
        return OK_C;

}

EN_cardError_t getCardExpiryDate(ST_cardData_t*cardData)
{
    char date[5] = {0};
    printf("Enter Expire Date : ");
    gets(date);
    strcpy(cardData->cardExpirationDate, date);
    if ((date == NULL) || (strlen(date) != 5) || (date[2] != '/') ||
        (date[0] < 48  && date[0] > 49) || (date[1] < 48 && date[1] > 57) ||
        (date[3] < 48 && date[3] > 57) || (date[4] < 48 && date[4] > 57))
        //Check that string in right format MM/YY
        return WRONG_EXP_DATE;
 
    else
        return OK_C;
      
}

EN_cardError_t getCardPAN(ST_cardData_t* cardData)
{
    char PAN[20] = {0};
    printf("Enter PAN : ");
    gets(PAN);
    strcpy(cardData->primaryAccountNumber, PAN);
    if ((PAN == NULL) || (strlen(PAN) > 19) || (strlen(PAN) < 16))
        // Check that length of PAN in range [16,19]
        return WRONG_PAN;

    else
        return OK_C;
}
