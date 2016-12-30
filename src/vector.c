#include "vector.h"

vector_t vector_vadd(vector_t lv, vector_t rv)
{
    vector_t result;
    
    result.x = lv.x + rv.x;
    result.y = lv.y + rv.y;
    result.z = lv.z + rv.z;

    return result;
}

vector_t vector_sadd(vector_t lv, vectorcp_t rv)
{
    vector_t result;
    
    result.x = lv.x + rv;
    result.y = lv.y + rv;
    result.z = lv.z + rv;

    return result;
}

vector_t vector_vsub(vector_t lv, vector_t rv)
{
    vector_t result;

    result.x = lv.x - rv.x;
    result.y = lv.y - rv.y;
    result.z = lv.z - rv.z;

    return result;
}

vector_t vector_ssub(vector_t lv, vectorcp_t rv)
{
    vector_t result;

    result.x = lv.x - rv;
    result.y = lv.y - rv;
    result.z = lv.z - rv;

    return result;
}

vector_t vector_vmul(vector_t lv, vector_t rv)
{
    vector_t result;

    result.x = lv.x * rv.x;
    result.y = lv.y * rv.y;
    result.z = lv.z * rv.z;

    return result;
}

vector_t vector_smul(vector_t lv, vectorcp_t rv)
{
    vector_t result;

    result.x = lv.x * rv;
    result.y = lv.y * rv;
    result.z = lv.z * rv;

    return result;
}

vector_t vector_vdiv(vector_t lv, vector_t rv)
{
    vector_t result;

    if(rv.x == 0) rv.x = 1;
    if(rv.y == 0) rv.y = 1;
    if(rv.z == 0) rv.z = 1;

    result.x = lv.x / rv.x;
    result.y = lv.y / rv.y;
    result.z = lv.z / rv.z;

    return result;
}

vector_t vector_sdiv(vector_t lv, vectorcp_t rv)
{
    vector_t result;

    if(rv == 0) rv = 1;

    result.x = lv.x / rv;
    result.y = lv.y / rv;
    result.z = lv.z / rv;

    return result;
}

vectorcp_t vector_get_magnitude(vector_t mag)
{
    vectorcp_t res = sqrt(mag.x * mag.x + mag.y * mag.y + mag.z * mag.z);
    
    return res;
}

vector_t vector_set_magnitude(vector_t v, vectorcp_t val)
{
    vector_t nv;
    
    nv = vector_normalize(v);
    nv = vector_smul(nv, val);

    return nv;
}

vector_t vector_normalize(vector_t v)
{
    vector_t nv;
    vectorcp_t mag;
    
    mag = vector_get_magnitude(v);
    nv = vector_sdiv(v, mag);
    
    return nv;
}

vectorcp_t vector_distance(vector_t v1, vector_t v2)
{
    vector_t nv;

    nv = vector_vsub(v1, v2);
    return vector_get_magnitude(nv);
}

vectorcp_t vector_dot(vector_t v1, vector_t v2)
{
    return ((v1.x * v2.x) + (v1.y * v2.y) + (v1.z * v2.z));
}