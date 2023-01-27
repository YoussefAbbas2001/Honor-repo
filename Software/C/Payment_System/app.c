#include "app.h"
#include <stdio.h>
#include "STD_TYPES.h"

#include "card.h"
#include "terminal.h"
#include "server.h"

void appStart(void)
{
	ST_cardData_t card;
	ST_terminalData_t terminal;
	ST_transaction_t transaction;

	terminal.maxTransAmount = 100000000000;

	if(getCardHolderName(&card) == OK_C)
	{
		if (getCardExpiryDate(&card) == OK_C)
		{
			if (getCardPAN(&card) == OK_C)
			{
				if (getTransactionDate(&terminal) == OK_T)
				{
					if (isCardExired(&card, terminal) == OK_T)
					{
						if (getTransactionAmount(&terminal) == OK_T)
						{
							if (isBelowMaxAmount(&terminal) == OK_T)
							{
								if (isValidAccount(&card) == OK_S)
								{
									transaction.cardHolderData = card;
									transaction.terminalData = terminal;
									if (recieveTransactionData(&transaction) == APPROVED)
									{
										printf("\nTransaction Done\n\n");
									}
									else
									{
										printf("\nError: FAIL IN TRANSACTION\n\n");
									}
									
								}
								else
								{
									printf("\nError: INVALID ACCOUNT\n\n");
								}
							}
							else
							{
								printf("\nError: AMOUNT EXCEEDING LIMIT\n\n");
							}
						}
						else
						{
							printf("\nError: WRONG TRANSACTION AMOUNT\n\n");
						}
					}
					else
					{
						printf("\nError: CARD EXPIRED\n\n");
					}
				}
				else
				{
					printf("\nError: WRONG TRANSACTION DATE\n\n");
				}
			}
			else
			{
				printf("\nError: WRONG PAN NUMBER\n\n");
			}
		}
		else
		{
			printf("\nError: WRONG EXPIRY DATE\n\n");
		}
	}
	else 
	{
		printf("\nError: WRONG NAME\n\n");
	}
}

int main()
{

	appStart();
	return 0;
}
