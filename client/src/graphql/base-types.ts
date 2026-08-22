export type Maybe<T> = T | null;
export type InputMaybe<T> = Maybe<T>;
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: { input: string; output: string; }
  String: { input: string; output: string; }
  Boolean: { input: boolean; output: boolean; }
  Int: { input: number; output: number; }
  Float: { input: number; output: number; }
  /** Date with time (isoformat) */
  DateTime: { input: string; output: string; }
  /** Represents NULL values */
  Void: { input: null; output: null; }
};

export type BasePaginationIn = {
  limit?: InputMaybe<Scalars['Int']['input']>;
  offset?: InputMaybe<Scalars['Int']['input']>;
};

export enum EUserRole {
  Student = 'STUDENT',
  Teacher = 'TEACHER'
}

export type IAppError = {
  message: Scalars['String']['output'];
};

export type IBaseMeta = {
  count: Scalars['Int']['output'];
};

export type IBaseType = {
  createdAt: Scalars['DateTime']['output'];
  id: Scalars['Int']['output'];
  updatedAt: Scalars['DateTime']['output'];
};

export type JwTs = {
  __typename?: 'JWTs';
  accessToken: Scalars['String']['output'];
  refreshToken: Scalars['String']['output'];
};

export type JwTsObjectNotFoundError = JwTs | ObjectNotFoundError;

export type JwTsUnauthorizedErrorObjectNotFoundError = JwTs | ObjectNotFoundError | UnauthorizedError;

export type Mutation = {
  __typename?: 'Mutation';
  login: JwTsObjectNotFoundError;
  logout?: Maybe<Scalars['Void']['output']>;
  refresh: JwTsUnauthorizedErrorObjectNotFoundError;
  userCreate: UserObjectAlreadyExistsError;
  userDelete?: Maybe<Scalars['Void']['output']>;
  userResetPasswordConfirm?: Maybe<ObjectNotFoundError>;
  userResetPasswordRequest?: Maybe<ObjectNotFoundError>;
  userUpdate: UserObjectAlreadyExistsErrorObjectNotFoundError;
};


export type MutationLoginArgs = {
  input: UserCredentialsIn;
};


export type MutationUserCreateArgs = {
  input: UserIn;
};


export type MutationUserDeleteArgs = {
  id: Scalars['Int']['input'];
};


export type MutationUserResetPasswordConfirmArgs = {
  code: Scalars['String']['input'];
  id: Scalars['Int']['input'];
};


export type MutationUserResetPasswordRequestArgs = {
  email: Scalars['String']['input'];
};


export type MutationUserUpdateArgs = {
  id: Scalars['Int']['input'];
  input: UserIn;
};

export type ObjectAlreadyExistsError = IAppError & {
  __typename?: 'ObjectAlreadyExistsError';
  message: Scalars['String']['output'];
};

export type ObjectNotFoundError = IAppError & {
  __typename?: 'ObjectNotFoundError';
  message: Scalars['String']['output'];
};

export type Query = {
  __typename?: 'Query';
  health: Scalars['Int']['output'];
  me: UserObjectNotFoundError;
  user: UserObjectNotFoundError;
  users: UsersMeta;
};


export type QueryUserArgs = {
  id: Scalars['Int']['input'];
};


export type QueryUsersArgs = {
  filters?: InputMaybe<UserFiltersIn>;
  pagination?: InputMaybe<BasePaginationIn>;
};

export type UnauthorizedError = IAppError & {
  __typename?: 'UnauthorizedError';
  message: Scalars['String']['output'];
};

export type User = IBaseType & {
  __typename?: 'User';
  createdAt: Scalars['DateTime']['output'];
  email: Scalars['String']['output'];
  id: Scalars['Int']['output'];
  isAdmin: Scalars['Boolean']['output'];
  name: Scalars['String']['output'];
  patronymic?: Maybe<Scalars['String']['output']>;
  role: EUserRole;
  surname: Scalars['String']['output'];
  updatedAt: Scalars['DateTime']['output'];
};

export type UserCredentialsIn = {
  email: Scalars['String']['input'];
  password: Scalars['String']['input'];
};

export type UserFiltersIn = {
  isAdmin?: InputMaybe<Scalars['Boolean']['input']>;
  role?: InputMaybe<EUserRole>;
  searchQuery?: InputMaybe<Scalars['String']['input']>;
};

export type UserIn = {
  email: Scalars['String']['input'];
  isAdmin: Scalars['Boolean']['input'];
  name: Scalars['String']['input'];
  patronymic?: InputMaybe<Scalars['String']['input']>;
  role: EUserRole;
  surname: Scalars['String']['input'];
};

export type UserObjectAlreadyExistsError = ObjectAlreadyExistsError | User;

export type UserObjectAlreadyExistsErrorObjectNotFoundError = ObjectAlreadyExistsError | ObjectNotFoundError | User;

export type UserObjectNotFoundError = ObjectNotFoundError | User;

export type UsersMeta = IBaseMeta & {
  __typename?: 'UsersMeta';
  count: Scalars['Int']['output'];
  users: Array<User>;
};
