#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "STD_TYPES.h"
#include "card.h"
#include "terminal.h"


EN_terminalError_t getTransactionDate(ST_terminalData_t* termData)
{
	uint8_t transction_date[11] = {0};
	printf("Enter trasnction Date : ");
	gets(transction_date);
	strcpy(termData->transactionDate, transction_date);
	if ((termData->transactionDate == NULL) || (termData->transactionDate[2] != '/') || (termData->transactionDate[5] != '/'))
		// Check in format DD/MM/YYYY
		return WRONG_DATE;
	else
		return OK_T;


}

EN_terminalError_t isCardExired(ST_cardData_t* cardData, ST_terminalData_t termData)
{
	uint8_t edited_date[5];
	edited_date[0] = termData.transactionDate[3];
	edited_date[1] = termData.transactionDate[4];
	edited_date[2] = termData.transactionDate[5];
	edited_date[3] = termData.transactionDate[8];
	edited_date[4] = termData.transactionDate[9];
	
	if (edited_date[3] < cardData->cardExpirationDate[3])
		return OK_T;
	else if ((edited_date[3] == cardData->cardExpirationDate[3]) && (edited_date[4] < cardData->cardExpirationDate[4]))
		return OK_T;
	else if ((edited_date[3] == cardData->cardExpirationDate[3]) && (edited_date[4] == cardData->cardExpirationDate[4]) && (edited_date[0] < cardData->cardExpirationDate[0]))
		return OK_T;
	else if ((edited_date[3] == cardData->cardExpirationDate[3]) && (edited_date[4] == cardData->cardExpirationDate[4]) && (edited_date[0] < cardData->cardExpirationDate[0]) && (edited_date[1] > cardData->cardExpirationDate[1]))
		return OK_T;
	else
		return EXPIRED_CARD;
}


EN_terminalError_t getTransactionAmount(ST_terminalData_t* termData)
{
	float trans_amount;

	printf("Enter Transaction Amount : ");
	scanf("%f", &trans_amount);
	termData->transAmount = trans_amount;
	if (trans_amount <= 0)
		return INVALID_AMOUNT;
	else
		return OK_T;
	
}

EN_terminalError_t isBelowMaxAmount(ST_terminalData_t* termData)
{
	if (termData->transAmount <= termData->maxTransAmount)
		return OK_T;
	else
		return EXCEED_MAX_AMOUNT;
}

EN_terminalError_t setMaxAmount(ST_terminalData_t* termData)
{
	float max_trans_amount;

	printf("Enter Transaction Amount : ");
	scanf("%f", &max_trans_amount);
	termData->maxTransAmount = max_trans_amount;
	if (max_trans_amount <= 0)
		return INVALID_MAX_AMOUNT;
	else
		return OK_T;
}
