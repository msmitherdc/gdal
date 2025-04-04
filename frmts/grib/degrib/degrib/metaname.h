#ifndef METANAME_H
#define METANAME_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "type.h"
#include "meta.h"

const char *centerLookup(unsigned short int center);

const char *subCenterLookup(unsigned short int center,
                            unsigned short int subcenter);

const char *processLookup(unsigned short int center, unsigned char process);

void ParseElemName (uChar mstrVersion, uShort2 center, uShort2 subcenter, int prodType,
                    int templat, int cat, int subcat, sInt4 lenTime,
                    uChar timeRangeUnit, uChar statProcessID,
                    uChar timeIncrType, uChar genID, uChar probType,
                    double lowerProb, double upperProb,
                    uChar derivedFcst,
                    char **name,
                    char **comment, char **unit, int *convert,
                    sChar percentile, uChar genProcess,
                    sChar f_fstValue, double fstSurfValue,
                    sChar f_sndValue, double sndSurfValue);

int ComputeUnit (int convert, char * origName, sChar f_unit, double *unitM,
                 double *unitB, char *name);
/*
int ComputeUnit (int prodType, int templat, int cat, int subcat, sChar f_unit,
                 double *unitM, double *unitB, char *name);
*/
int Table45Lookup (int code, uShort2 center, uShort2 subcenter,
                   int *f_reserved,
                   const char** shortName, const char** name, const char** unit);

int IsData_NDFD (unsigned short int center, unsigned short int subcenter);

int IsData_MOS (unsigned short int center, unsigned short int subcenter);

void ParseLevelName (unsigned short int center, unsigned short int subcenter,
                     uChar surfType, double value, sChar f_sndValue,
                     double sndValue, char **shortLevelName,
                     char **longLevelName);

void MetanameCleanup(void);

#ifdef __cplusplus
}
#endif  /* __cplusplus */

#endif /* METANAME_H */
