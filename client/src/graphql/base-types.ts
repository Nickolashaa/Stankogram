export type Maybe<T> = T | null
export type InputMaybe<T> = Maybe<T>
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: { input: string; output: string }
  String: { input: string; output: string }
  Boolean: { input: boolean; output: boolean }
  Int: { input: number; output: number }
  Float: { input: number; output: number }
  /** Date with time (isoformat) */
  DateTime: { input: string; output: string }
  /** Represents NULL values */
  Void: { input: null; output: null }
}

export type BasePaginationIn = {
  limit?: InputMaybe<Scalars["Int"]["input"]>
  offset?: InputMaybe<Scalars["Int"]["input"]>
}

export type Chat = IBaseType & {
  __typename?: "Chat"
  createdAt: Scalars["DateTime"]["output"]
  id: Scalars["Int"]["output"]
  lastMessage?: Maybe<Message>
  participants: Array<ChatParticipant>
  title: Scalars["String"]["output"]
  type: EChatType
  updatedAt: Scalars["DateTime"]["output"]
}

export type ChatFiltersIn = {
  type?: InputMaybe<EChatType>
}

export type ChatInvalidInputErrorObjectNotFoundError =
  Chat | InvalidInputError | ObjectNotFoundError

export type ChatInvalidInputErrorObjectNotFoundErrorObjectAlreadyExistsError =
  Chat | InvalidInputError | ObjectAlreadyExistsError | ObjectNotFoundError

export type ChatParticipant = IBaseType &
  IChat &
  IUser & {
    __typename?: "ChatParticipant"
    chat: Chat
    createdAt: Scalars["DateTime"]["output"]
    id: Scalars["Int"]["output"]
    isAdmin: Scalars["Boolean"]["output"]
    isMuted: Scalars["Boolean"]["output"]
    lastReadAt?: Maybe<Scalars["DateTime"]["output"]>
    updatedAt: Scalars["DateTime"]["output"]
    user: User
  }

export type ChatParticipantIn = {
  chatId: Scalars["Int"]["input"]
  isAdmin: Scalars["Boolean"]["input"]
  isMuted: Scalars["Boolean"]["input"]
  userId: Scalars["Int"]["input"]
}

export type ChatParticipantObjectNotFoundError = ChatParticipant | ObjectNotFoundError

export type ChatParticipantObjectNotFoundErrorObjectAlreadyExistsErrorInvalidInputError =
  ChatParticipant | InvalidInputError | ObjectAlreadyExistsError | ObjectNotFoundError

export type ChatUpdateIn = {
  title: Scalars["String"]["input"]
}

export type ChatsMeta = IBaseMeta & {
  __typename?: "ChatsMeta"
  chats: Array<Chat>
  count: Scalars["Int"]["output"]
}

export type ChatsMetaUnauthorizedError = ChatsMeta | UnauthorizedError

export enum EChatType {
  Private = "PRIVATE",
  Public = "PUBLIC",
}

export enum EMessageType {
  Text = "TEXT",
}

export enum EUserRole {
  Student = "STUDENT",
  Teacher = "TEACHER",
}

export type IAppError = {
  message: Scalars["String"]["output"]
}

export type IBaseMeta = {
  count: Scalars["Int"]["output"]
}

export type IBaseType = {
  createdAt: Scalars["DateTime"]["output"]
  id: Scalars["Int"]["output"]
  updatedAt: Scalars["DateTime"]["output"]
}

export type IChat = {
  chat: Chat
}

export type IUser = {
  user: User
}

export type InvalidInputError = IAppError & {
  __typename?: "InvalidInputError"
  message: Scalars["String"]["output"]
}

export type JwTs = {
  __typename?: "JWTs"
  accessToken: Scalars["String"]["output"]
  refreshToken: Scalars["String"]["output"]
}

export type JwTsObjectNotFoundError = JwTs | ObjectNotFoundError

export type JwTsUnauthorizedErrorObjectNotFoundError =
  JwTs | ObjectNotFoundError | UnauthorizedError

export type Message = IBaseType &
  IChat &
  IUser & {
    __typename?: "Message"
    chat: Chat
    createdAt: Scalars["DateTime"]["output"]
    id: Scalars["Int"]["output"]
    text: Scalars["String"]["output"]
    type: EMessageType
    updatedAt: Scalars["DateTime"]["output"]
    user: User
  }

export type MessageFiltersIn = {
  chatId: Scalars["Int"]["input"]
  type?: InputMaybe<EMessageType>
}

export type MessageIn = {
  chatId: Scalars["Int"]["input"]
  text: Scalars["String"]["input"]
  type: EMessageType
}

export type MessageObjectNotFoundError = Message | ObjectNotFoundError

export type MessagesMeta = IBaseMeta & {
  __typename?: "MessagesMeta"
  count: Scalars["Int"]["output"]
  messages: Array<Message>
}

export type Mutation = {
  __typename?: "Mutation"
  addParticipantToChat: ChatParticipantObjectNotFoundErrorObjectAlreadyExistsErrorInvalidInputError
  createMessage: MessageObjectNotFoundError
  createPrivateChat: ChatInvalidInputErrorObjectNotFoundErrorObjectAlreadyExistsError
  createPublicChat: ChatInvalidInputErrorObjectNotFoundErrorObjectAlreadyExistsError
  createSystemNotification: SystemNotification
  login: JwTsObjectNotFoundError
  logout?: Maybe<Scalars["Void"]["output"]>
  markChatRead: ChatParticipantObjectNotFoundError
  markSystemNotificationRead?: Maybe<ObjectNotFoundError>
  refresh: JwTsUnauthorizedErrorObjectNotFoundError
  removeParticipantFromChat?: Maybe<Scalars["Void"]["output"]>
  updateChat: ChatInvalidInputErrorObjectNotFoundError
  updateChatParticipantPermissions: ChatParticipantObjectNotFoundError
  updateSystemNotification: SystemNotificationObjectNotFoundError
  userCreate: UserObjectAlreadyExistsError
  userDelete?: Maybe<Scalars["Void"]["output"]>
  userResetPasswordConfirm?: Maybe<ObjectNotFoundError>
  userResetPasswordRequest?: Maybe<ObjectNotFoundError>
  userUpdate: UserObjectAlreadyExistsErrorObjectNotFoundError
}

export type MutationAddParticipantToChatArgs = {
  input: ChatParticipantIn
}

export type MutationCreateMessageArgs = {
  input: MessageIn
}

export type MutationCreatePrivateChatArgs = {
  input: PrivateChatIn
}

export type MutationCreatePublicChatArgs = {
  input: PublicChatIn
}

export type MutationCreateSystemNotificationArgs = {
  input: SystemNotificationIn
}

export type MutationLoginArgs = {
  input: UserCredentialsIn
}

export type MutationMarkChatReadArgs = {
  chatId: Scalars["Int"]["input"]
}

export type MutationMarkSystemNotificationReadArgs = {
  id: Scalars["Int"]["input"]
}

export type MutationRemoveParticipantFromChatArgs = {
  chatId: Scalars["Int"]["input"]
  userId: Scalars["Int"]["input"]
}

export type MutationUpdateChatArgs = {
  chatId: Scalars["Int"]["input"]
  input: ChatUpdateIn
}

export type MutationUpdateChatParticipantPermissionsArgs = {
  input: ChatParticipantIn
}

export type MutationUpdateSystemNotificationArgs = {
  id: Scalars["Int"]["input"]
  input: SystemNotificationIn
}

export type MutationUserCreateArgs = {
  input: UserIn
}

export type MutationUserDeleteArgs = {
  id: Scalars["Int"]["input"]
}

export type MutationUserResetPasswordConfirmArgs = {
  code: Scalars["String"]["input"]
  id: Scalars["Int"]["input"]
}

export type MutationUserResetPasswordRequestArgs = {
  email: Scalars["String"]["input"]
}

export type MutationUserUpdateArgs = {
  id: Scalars["Int"]["input"]
  input: UserIn
}

export type ObjectAlreadyExistsError = IAppError & {
  __typename?: "ObjectAlreadyExistsError"
  message: Scalars["String"]["output"]
}

export type ObjectNotFoundError = IAppError & {
  __typename?: "ObjectNotFoundError"
  message: Scalars["String"]["output"]
}

export type PrivateChatIn = {
  participantId: Scalars["Int"]["input"]
}

export type PublicChatIn = {
  participantIds?: InputMaybe<Array<Scalars["Int"]["input"]>>
  title: Scalars["String"]["input"]
}

export type Query = {
  __typename?: "Query"
  chats: ChatsMeta
  health: Scalars["Int"]["output"]
  me: UserObjectNotFoundError
  meChats: ChatsMetaUnauthorizedError
  meSystemNotifications: SystemNotificationsMeta
  messages: MessagesMeta
  systemNotifications: SystemNotificationsMeta
  users: UsersMeta
}

export type QueryChatsArgs = {
  filters?: InputMaybe<ChatFiltersIn>
  pagination?: InputMaybe<BasePaginationIn>
}

export type QueryMeChatsArgs = {
  filters?: InputMaybe<ChatFiltersIn>
  pagination?: InputMaybe<BasePaginationIn>
}

export type QueryMeSystemNotificationsArgs = {
  filters?: InputMaybe<SystemNotificationFiltersIn>
  pagination?: InputMaybe<BasePaginationIn>
}

export type QueryMessagesArgs = {
  filters: MessageFiltersIn
  pagination?: InputMaybe<BasePaginationIn>
}

export type QuerySystemNotificationsArgs = {
  pagination?: InputMaybe<BasePaginationIn>
}

export type QueryUsersArgs = {
  filters?: InputMaybe<UserFiltersIn>
  pagination?: InputMaybe<BasePaginationIn>
}

export type Subscription = {
  __typename?: "Subscription"
  events: Message
}

export type SystemNotification = IBaseType & {
  __typename?: "SystemNotification"
  createdAt: Scalars["DateTime"]["output"]
  id: Scalars["Int"]["output"]
  text: Scalars["String"]["output"]
  updatedAt: Scalars["DateTime"]["output"]
}

export type SystemNotificationFiltersIn = {
  onlyUnread?: InputMaybe<Scalars["Boolean"]["input"]>
}

export type SystemNotificationIn = {
  text: Scalars["String"]["input"]
}

export type SystemNotificationObjectNotFoundError = ObjectNotFoundError | SystemNotification

export type SystemNotificationsMeta = IBaseMeta & {
  __typename?: "SystemNotificationsMeta"
  count: Scalars["Int"]["output"]
  systemNotifications: Array<SystemNotification>
}

export type UnauthorizedError = IAppError & {
  __typename?: "UnauthorizedError"
  message: Scalars["String"]["output"]
}

export type User = IBaseType & {
  __typename?: "User"
  createdAt: Scalars["DateTime"]["output"]
  email: Scalars["String"]["output"]
  fullName: Scalars["String"]["output"]
  id: Scalars["Int"]["output"]
  isAdmin: Scalars["Boolean"]["output"]
  name: Scalars["String"]["output"]
  patronymic?: Maybe<Scalars["String"]["output"]>
  role: EUserRole
  surname: Scalars["String"]["output"]
  updatedAt: Scalars["DateTime"]["output"]
}

export type UserCredentialsIn = {
  email: Scalars["String"]["input"]
  password: Scalars["String"]["input"]
}

export type UserFiltersIn = {
  isAdmin?: InputMaybe<Scalars["Boolean"]["input"]>
  role?: InputMaybe<EUserRole>
  searchQuery?: InputMaybe<Scalars["String"]["input"]>
}

export type UserIn = {
  email: Scalars["String"]["input"]
  isAdmin: Scalars["Boolean"]["input"]
  name: Scalars["String"]["input"]
  patronymic?: InputMaybe<Scalars["String"]["input"]>
  role: EUserRole
  surname: Scalars["String"]["input"]
}

export type UserObjectAlreadyExistsError = ObjectAlreadyExistsError | User

export type UserObjectAlreadyExistsErrorObjectNotFoundError =
  ObjectAlreadyExistsError | ObjectNotFoundError | User

export type UserObjectNotFoundError = ObjectNotFoundError | User

export type UsersMeta = IBaseMeta & {
  __typename?: "UsersMeta"
  count: Scalars["Int"]["output"]
  users: Array<User>
}
