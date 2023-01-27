#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "STD_TYPES.h"
#include "card.h"
#include "terminal.h"
#include "server.h"

extern ST_accountsDB_t  accounts_database[2] = { {100000, "BJQPP5524G5433422"}, {14500000,"AAAAAA12345678AB"}};


extern ST_transaction_t transactions_database[255] = {0};

EN_transStat_t recieveTransactionData(ST_transaction_t* transData)
{
    int indx = -1;

    for (int i = 0; i < sizeof(accounts_database) / sizeof(ST_accountsDB_t); i++)
    {
        // search for the account
        if ( strcmp(transData->cardHolderData.primaryAccountNumber, accounts_database[i].primaryAccountNumber) == 0)
        {
            indx = i;
            break; 
        }
    }

    if (indx == -1)
    {
        transData->transState = DECLINED_STOLEN_CARD;
        
    }
    else 
    {
        if (accounts_database[indx].balance < transData->terminalData.transAmount)
        {
            transData->transState = DECLINED_INSUFFECIENT_FUND;
        }
        else if (accounts_database[indx].balance > transData->terminalData.transAmount)
        {
            
            printf("Balance Before Transaction : %f\n", accounts_database[indx].balance);
            accounts_database[indx].balance = accounts_database[indx].balance - transData->terminalData.transAmount;
            //transactions_database[transData->transactionSequenceNumber] = *transData;
            //transData->transactionSequenceNumber++;
            printf("Balance After Transaction : %f\n", accounts_database[indx].balance);
            transData->transState = APPROVED;
        }
        else
        {
            transData->transState = INTERNAL_SERVER_ERROR;
        }
    }
    return transData->transState;

}


EN_serverError_t isValidAccount(ST_cardData_t* cardData)
{
    int indx = -1;
    for (int i = 0; i < sizeof(accounts_database) / sizeof(ST_accountsDB_t); i++)
    {
        // search for the account
        if (strcmp(cardData->primaryAccountNumber, accounts_database[i].primaryAccountNumber) == 0)
        {
            indx = i;
            break;
        }
    }
    
    if (indx == -1)
        return DECLINED_STOLEN_CARD;
    else
        return OK_S;
}

EN_serverError_t isAmountAvailable(ST_transaction_t* transData)
{
    int indx = -1;
    for (int i = 0; i < sizeof(accounts_database) / sizeof(ST_accountsDB_t); i++)
    {
        // search for the account
        if (strcmp(transData->cardHolderData.primaryAccountNumber, accounts_database[i].primaryAccountNumber) == 0)
        {
            indx = i;
            break;
        }
    }
   
    if (indx == -1)
        return ACCOUNT_NOT_FOUND;
    if (transData->terminalData.transAmount > accounts_database[indx].balance)
    {
 
        return LOW_BALANCE;
    }
    else
    {
     
        return OK_S;
    }
}

EN_serverError_t saveTransaction(ST_transaction_t* transData)
{
    int indx = -1;
    for (int i = 0; i < sizeof(accounts_database) / sizeof(ST_accountsDB_t); i++)
    {
        // search for the account
        if (strcmp(transData->cardHolderData.primaryAccountNumber, accounts_database[i].primaryAccountNumber) == 0)
        {
            indx = i;
            break;
        }
    }
    if (isAmountAvailable(transData) == OK_S)
    {
        accounts_database[indx].balance = accounts_database[indx].balance - transData->terminalData.transAmount;
        transData->transactionSequenceNumber++;
        transactions_database[transData->transactionSequenceNumber] = *transData;
        return OK_S;
    }
    else if (isAmountAvailable(transData) == LOW_BALANCE)
        return SAVING_FAILED;

    else
        return ACCOUNT_NOT_FOUND;
 
}

ST_transaction_t getTransaction(uint32_t transactionSquenceNumber)
{
    return transactions_database[transactionSquenceNumber];
}
