const API = 'http://localhost:4242/';
const APIMEDIA = API + 'media/';
const APICREATE = API + 'api/create';
const APIDELETE = API + 'api/delete';
const APICOMPUTE = API + 'api/compute';
const APITRAIN = API + 'api/train';
const APIINFERENCE = API + 'api/inference';
const APIINITIALIZE = API + 'api/initialize';

export async function fetchApi(queries: object, api: string) {
   // WHY USING BLOB? WELL, OTHERWISE WE CANT PUSH MULTIPLIE FILES OR WE HAVE
  // TO WRITE EXCEPTIONS ON THE BACKEND SIDE ... MAYBE THERE IS A BETTER SOLUTION
  const formData = new FormData();
  formData.append(
    'queries',
    new Blob([JSON.stringify(queries)], { type: 'application/json' })
  );

  return fetch(api, {
    method: 'POST',
    body: formData
  }).then(response => {    
    if (response.status >= 400) {
      return { placeholder: 'Something went wrong!' };
    }
    return response.json();
  });
}

export async function fetchApiMediaText(filepath: string) {
  // var url = new URL(APIMEDIA + filepath);
  return fetch(APIMEDIA + filepath, {
    method: 'GET'
  }).then((response: any) => {
    if (response.status >= 400) {
      return { placeholder: 'Something went wrong!' };
    }
    return response.text();
  });
}

export async function fetchApiUpload(queries: object, files: string) {
  // var url = new URL(APICREATE);
  const formData = new FormData();
  formData.append(
    'queries',
    new Blob([JSON.stringify(queries)], { type: 'application/json' })
  );
  for (let i = 0; i < files.length; i++) {
    formData.append('files', files[i]);
  }
  return fetch(APICREATE, {
    method: 'POST',
    body: formData
  }).then(response => {
    if (response.status >= 400) {
      return { placeholder: 'Something went wrong!' };
    }
    return response.json();
  });
}

export async function getData(queries: object) {
  return fetchApi(queries, APICOMPUTE).then(resultset => {
    return resultset;
  });
}

export async function createData(queries: object) {
  return fetchApi(queries, APICREATE).then(resultsets => {
    return resultsets;
  });
}

export async function createDataUpload(queries: object, files: BinaryType) {
  return fetchApiUpload(queries, files).then(resultset => {
    return resultset;
  });
}

export async function removeData(queries: object) {
  return fetchApi(queries, APIDELETE).then(resultset => {
    return resultset;
  });
}

export async function trainAiModule(queries: object) {
  return fetchApi(queries, APITRAIN).then(resultset => {
    return resultset;
  });
}

export async function inferenceData(queries: object) {
  return fetchApi(queries, APIINFERENCE).then(resultset => {
    return resultset;
  });
}

export async function initializeAiModule(queries: object) {
  return fetchApi(queries, APIINITIALIZE).then(resultset => {
    return resultset;
  });
}
